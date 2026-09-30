"""Offline checks. These tests never invoke Clay or start a model run."""
import argparse
import contextlib
import importlib.machinery
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

loader = importlib.machinery.SourceFileLoader('runner', str(Path(__file__).with_name('eval')))
spec = importlib.util.spec_from_loader(loader.name, loader)
runner = importlib.util.module_from_spec(spec)
loader.exec_module(runner)


class RunnerTests(unittest.TestCase):
    def test_tool_trace_not_self_report(self):
        record = {'case_id': 'x', 'arm': 'B', 'node_id': 'n'}
        result = {'nodes': [{'nodeId': 'n', 'outputs': {
            'structuredOutputs': {'response': 'I used Keenable'}, 'stepsTaken': ['Used searchGoogle {}. The results are: none']}}]}
        self.assertFalse(runner.summarize(result, record)['keenable_tool_used'])
        result['nodes'][0]['outputs']['stepsTaken'] = ['Used arbitrary-prefix-fetch_page_content {}. The results are: example']
        self.assertTrue(runner.summarize(result, record)['keenable_tool_used'])
        del result['nodes'][0]['outputs']['stepsTaken']
        self.assertIsNone(runner.summarize(result, record)['keenable_tool_used'])

    def test_native_google_trace_counts(self):
        record = {'case_id': 'x', 'arm': 'B', 'node_id': 'n'}
        steps = ['Searched Google with query "Keenable funding". The results are: {}'] * 3
        steps += ['Used visitWebpage {"url":"https://example.com"}. The results are: {}'] * 3
        steps += ['Used keenable-public-evaluation-search_web_pages {"query":"funding"}. The results are: {}']
        result = {'nodes': [{'nodeId': 'n', 'outputs': {'stepsTaken': steps}}]}
        summary = runner.summarize(result, record)
        self.assertEqual(summary['research_tool_call_count'], 7)
        self.assertEqual(summary['native_search_calls'], 3)
        self.assertEqual(summary['native_fetch_calls'], 3)
        self.assertEqual(summary['keenable_calls'], 1)

    def test_refresh_restores_only_builder_formatting(self):
        import copy
        with tempfile.TemporaryDirectory() as temporary:
            state = {'configuration_hash': runner.digest({'prompt': 'Research {{domain}}.\n'}),
                     'arms': {'B': {'workflow_id': 'w', 'trigger_node_id': 't', 'node_id': 'old'}}}
            cfg = {'prompt': 'Research {{domain}}.\n'}
            nodes = {'t': {'id': 't'}, 'old': {'id': 'old', 'agentClaygentId': 'c',
                     'agentPrompt': 'Research {{domain}}.  ', 'incomingEdges': [{'sourceNode': 't'}]}}
            mutations = []
            def fake_cli(*args, **kwargs):
                if args[:3] == ('workflows', 'graph', 'get'):
                    return {'nodes': list(nodes.values()), 'summary': {'edges': [
                        {'sourceNodeId': edge['sourceNode'], 'targetNodeId': name}
                        for name, node in nodes.items() for edge in node.get('incomingEdges', [])]}}
                if args[:3] == ('workflows', 'nodes', 'get'):
                    return {'node': copy.deepcopy(nodes[args[4]])}
                self.fail(f'Unexpected CLI call: {args}')
            def fake_mutation(saved, label, args, payload=None):
                mutations.append((label, args, payload))
                if args[2] == 'create':
                    self.assertEqual(payload['agentClaygentId'], 'c')
                    self.assertNotIn('agentPrompt', payload)
                    nodes['new'] = dict(nodes['old'], id='new', incomingEdges=[])
                    return {'nodeId': 'new'}
                if args[2] == 'update':
                    nodes[args[4]].update(payload)
                else:
                    del nodes[args[4]]
                return {}
            def verify(saved, configuration):
                self.assertEqual(nodes['new']['agentPrompt'], cfg['prompt'])
                self.assertEqual(saved['arms']['B']['node_id'], 'new')
                self.assertNotIn('old', nodes)
            with patch.object(runner, 'STATE', Path(temporary) / 'state.json'), \
                 patch.object(runner, 'state_read', return_value=state), patch.object(runner, 'config', return_value=cfg), \
                 patch.object(runner, 'cli', side_effect=fake_cli), patch.object(runner, 'mutation', side_effect=fake_mutation), \
                 patch.object(runner, 'preflight', side_effect=verify), contextlib.redirect_stdout(io.StringIO()):
                runner.refresh()
            prompt_updates = [payload for label, _, payload in mutations if label == 'restore B prompt formatting']
            self.assertEqual(prompt_updates, [{'agentPrompt': cfg['prompt']}])

    def test_paired_order_resume_hash_and_offline_replay(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            cases = [dict(id=f'c{i}', company_name=f'Company {i}', domain=f'c{i}.test',
                          as_of='2026-09-30', task_type='funding_and_lifecycle') for i in range(2)]
            cases[1]['task_type'] = 'entity_resolution'
            runner.save(root / 'cases.json', cases)
            state = {'workspace_id': 'test', 'arms': {arm: {'workflow_id': arm, 'node_id': arm} for arm in 'AB'}}
            cfg = {'prompt': 'test', 'model': 'test', 'schema': {}}
            calls = []
            def fake_cli(*args, **kwargs):
                calls.append(args)
                if args[:3] == ('workflows', 'runs', 'test'):
                    return {'runId': f'run-{len(calls)}', 'status': 'pending'}
                if args[:3] == ('workflows', 'runs', 'get'):
                    return {'runId': args[4], 'status': 'completed', 'dataCreditsUsed': 0.1,
                            'actionCreditsUsed': 1, 'nodes': [{'nodeId': args[3], 'outputs': {
                                'stepsTaken': [], 'structuredOutputs': {'company_identity': 'example'}}}]}
                self.fail(f'Unexpected CLI call: {args}')
            args = argparse.Namespace(concurrency=2, limit=2, stop_after_pairs=None, output=root / 'results', allow_credit_use=True, timeout=1)
            with patch.object(runner, 'ROOT', root), patch.object(runner, 'state_read', return_value=state), \
                 patch.object(runner, 'config', return_value=cfg), patch.object(runner, 'preflight', return_value={}), \
                 patch.object(runner, 'cli', side_effect=fake_cli), contextlib.redirect_stdout(io.StringIO()):
                runner.run(args)
                self.assertEqual([c[3] for c in calls if c[2] == 'test'], ['A', 'B', 'B', 'A'])
                count = len(calls)
                runner.run(args)
                self.assertEqual(len(calls), count, 'Resume must not submit completed runs again')
                first = (args.output / 'summary.json').read_bytes()
                first_table = (args.output / 'results.md').read_bytes()
                runner.reproduce(args.output)
                self.assertEqual(first, (args.output / 'summary.json').read_bytes())
                self.assertEqual(first_table, (args.output / 'results.md').read_bytes())
                self.assertIn(b'[ungraded](01-A/result.json)', first_table)
                self.assertFalse(runner.read(args.output / 'summary.json')['accuracy']['calculated'])
                cases[0]['domain'] = 'changed.test'
                runner.save(root / 'cases.json', cases)
                with self.assertRaisesRegex(RuntimeError, 'Resume rejected'):
                    runner.run(args)
                self.assertEqual(len(calls), count)
                runner.save(args.output / 'judgments.json', {'cases': [
                    {'case_id': 'c0', 'arm': 'A', 'scored_task': 'funding_and_lifecycle',
                     'fields': {'funding_stage': True}, 'supported_answer': False},
                    {'case_id': 'c1', 'arm': 'B', 'scored_task': 'entity_resolution',
                     'fields': {'identity': True}, 'supported_answer': True}]})
                runner.reproduce(args.output)
                groups = runner.read(args.output / 'summary.json')['accuracy']['by_arm']
                self.assertEqual(groups['A']['fields']['funding_stage'], {'correct': 1, 'total': 1})
                self.assertEqual(groups['B']['supported_answer']['total'], 0)
                self.assertIn('[1/1](01-A/result.json)', (args.output / 'results.md').read_text())

    def test_judgment_coverage_pairs_and_separate_entity_metrics(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'judgments.json'
            ids = ['keenable', 'tie', 'different_fields', 'missing_arm', 'freeman_seattle']
            manifest = {'runs': [{'case_id': case, 'arm': arm, 'inputs': {
                'task_type': 'entity_resolution' if case == 'freeman_seattle' else 'funding_and_lifecycle'}}
                for case in ids for arm in 'AB']}
            rows = [{'case_id': record['case_id'], 'arm': record['arm']} for record in manifest['runs']]
            fields = {
                ('keenable', 'A'): {'stage': False, 'date': True},
                ('keenable', 'B'): {'stage': True, 'date': True},
                ('tie', 'A'): {'stage': True, 'date': False, 'amount': None},
                ('tie', 'B'): {'stage': True, 'date': False, 'amount': None},
                ('different_fields', 'A'): {'stage': True, 'amount': None},
                ('different_fields', 'B'): {'stage': True, 'amount': True},
                ('missing_arm', 'A'): {'stage': False},
                ('freeman_seattle', 'A'): {'identity': False},
                ('freeman_seattle', 'B'): {'identity': True}}
            judgments = {'cases': [{'case_id': case, 'arm': arm,
                'scored_task': 'entity_resolution' if case == 'freeman_seattle' else 'funding_and_lifecycle',
                'fields': value, 'supported_answer': all(v for v in value.values() if v is not None),
                'wrong_claims': ['Extra claim for human review'], 'unsupported_claims': ['Extra claim']}
                for (case, arm), value in fields.items()]}
            runner.save(path, judgments)
            result = runner.judge_summary(path, manifest, rows)
            self.assertFalse(result['complete_judgment_coverage'])
            self.assertEqual(result['accuracy_status'], 'partial')
            self.assertEqual(result['by_arm']['A']['all_target_fields_correct'], {'correct': 1, 'total': 4})
            self.assertEqual(result['by_arm']['B']['all_target_fields_correct'], {'correct': 2, 'total': 3})
            pairs = result['paired_cases']
            self.assertEqual([pairs[x] for x in ('A_wins', 'B_wins', 'ties', 'incomparable')], [0, 1, 1, 2])
            self.assertEqual(result['excluding_keenable']['paired_cases']['B_wins'], 0)
            entity = result['entity_resolution']
            self.assertTrue(entity['complete_judgment_coverage'])
            self.assertEqual(entity['paired_cases']['B_wins'], 1)
            self.assertNotIn('identity', result['by_arm']['A']['fields'])
            self.assertEqual(result['by_arm']['A']['fields']['stage'], {'correct': 2, 'total': 4})
            judgments['cases'].append({'case_id': 'missing_arm', 'arm': 'B', 'scored_task': 'funding_and_lifecycle',
                                       'fields': {'stage': True}, 'supported_answer': True})
            runner.save(path, judgments)
            complete = runner.judge_summary(path, manifest, rows)
            self.assertTrue(complete['complete_judgment_coverage'])
            self.assertEqual(complete['accuracy_status'], 'complete')
            self.assertEqual(complete['paired_cases']['incomparable'], 1)

    def test_ambiguous_submission_never_retries(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            runner.save(root / 'cases.json', [dict(id='x', company_name='X', domain='x.test',
                        as_of='2026-09-30', task_type='funding_and_lifecycle')])
            state = {'workspace_id': 'test', 'arms': {a: {'workflow_id': a, 'node_id': a} for a in 'AB'}}
            args = argparse.Namespace(concurrency=2, limit=1, stop_after_pairs=None, output=root / 'run', allow_credit_use=True, timeout=1)
            with patch.object(runner, 'ROOT', root), patch.object(runner, 'state_read', return_value=state), \
                 patch.object(runner, 'config', return_value={}), patch.object(runner, 'preflight', return_value={}), \
                 patch.object(runner, 'cli', side_effect=RuntimeError('network lost')) as mock:
                with self.assertRaisesRegex(RuntimeError, 'network lost'):
                    runner.run(args)
                with self.assertRaisesRegex(RuntimeError, 'Ambiguous submission'):
                    runner.run(args)
                self.assertEqual(mock.call_count, 1)

    def test_fifty_case_plan_checkpoint_and_resume(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            cases = [dict(id=f'c{i}', company_name=f'Company {i}', domain=f'c{i}.test',
                          as_of='2026-09-30', task_type='funding_and_lifecycle') for i in range(50)]
            runner.save(root / 'cases.json', cases)
            state = {'workspace_id': 'test', 'arms': {a: {'workflow_id': a, 'node_id': a} for a in 'AB'}}
            submissions = []
            in_flight = set()
            current_cap = [2]
            fail_first_poll = [True]
            def fake_cli(*args, **kwargs):
                if args[2] == 'test':
                    submissions.append((args[3], kwargs['payload']['company_name']))
                    run_id = f'r{len(submissions)}'
                    in_flight.add(run_id)
                    self.assertLessEqual(len(in_flight), current_cap[0])
                    return {'runId': run_id, 'status': 'pending'}
                if fail_first_poll[0]:
                    fail_first_poll[0] = False
                    raise RuntimeError('poll transport lost')
                in_flight.remove(args[4])
                return {'runId': args[4], 'status': 'completed', 'nodes': []}
            args = argparse.Namespace(concurrency=2, limit=None, stop_after_pairs=1, output=root / 'run',
                                      allow_credit_use=True, timeout=1)
            with patch.object(runner, 'ROOT', root), patch.object(runner, 'state_read', return_value=state), \
                 patch.object(runner, 'config', return_value={}), patch.object(runner, 'preflight', return_value={}), \
                 patch.object(runner, 'cli', side_effect=fake_cli), contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaisesRegex(RuntimeError, 'poll transport lost'):
                    runner.run(args)
                self.assertEqual(len(submissions), 2)
                runner.run(args)
                # Simulate the first live manifest created before concurrency
                # became an operational setting. Its snapshot must stay intact.
                legacy = runner.read(args.output / 'manifest.json')
                legacy['frozen']['concurrency'] = 2
                legacy['frozen_hash'] = runner.digest(legacy['frozen'])
                runner.save(args.output / 'manifest.json', legacy)
                before = runner.read(args.output / 'manifest.json')
                self.assertEqual(len(before['runs']), 100)
                self.assertEqual(len(submissions), 2)
                runner.run(args)
                self.assertEqual(len(submissions), 2, 'Repeating checkpoint cannot start pair two')
                args.limit = 50
                args.stop_after_pairs = None
                args.concurrency = 4
                current_cap[0] = 4
                runner.run(args)
                after = runner.read(args.output / 'manifest.json')
                self.assertEqual(before['frozen_hash'], after['frozen_hash'])
                self.assertEqual(before['frozen'], after['frozen'])
                self.assertEqual([x['concurrency'] for x in after['execution_history']], [2, 2, 2, 4])
                self.assertEqual(len(submissions), 100)
                self.assertEqual(submissions[:4], [('A', 'Company 0'), ('B', 'Company 0'),
                                                  ('B', 'Company 1'), ('A', 'Company 1')])
                self.assertTrue(all(record['status'] == 'completed' for record in after['runs']))
                self.assertFalse(in_flight)
                args.limit = 51
                with self.assertRaisesRegex(RuntimeError, 'no larger than the case count'):
                    runner.run(args)
                self.assertEqual(len(submissions), 100)


if __name__ == '__main__':
    unittest.main()
