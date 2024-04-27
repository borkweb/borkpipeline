from pypipeline.pipeline import Pipeline
import unittest

class TestPipeline(unittest.TestCase):


    def test_it_runs_a_pipeline_with_callables(self):
        pipeline = Pipeline()
        result = pipeline.send('a sample string that is passed through to all pipes.       ') \
            .through([str.title, str.strip]) \
            .then_return()
        self.assertEqual('A Sample String That Is Passed Through To All Pipes.', result)

    def test_it_runs_a_pipeline_with_callables_and_executes_the_destination(self):
        pipeline = Pipeline()
        result = pipeline.send('a sample string that is passed through to all pipes.       ') \
            .through([str.title, str.strip]) \
            .then(lambda x: x.replace('A Sample', 'A Nice Long'))
        self.assertEqual('A Nice Long String That Is Passed Through To All Pipes.', result)

    def test_it_runs_a_pipeline_with_callables_and_closures(self):
        pipeline = Pipeline()
        result = pipeline.send('a sample string that is passed through to all pipes.       ') \
            .through([
                lambda x, next: next(x.replace('all', 'all the')),
                str.title,
                str.strip
            ]) \
            .then_return()
        self.assertEqual('A Sample String That Is Passed Through To All The Pipes.', result)

    def test_it_runs_a_pipeline_with_closures(self):
        pipeline = Pipeline()
        result = pipeline.send('a sample string that is passed through to all pipes.') \
            .through([
                lambda x, next: next(x.title()),
                lambda x, next: next(x.replace('All', 'All The'))
            ]) \
            .then_return()
        self.assertEqual('A Sample String That Is Passed Through To All The Pipes.', result)

    def test_it_runs_a_pipeline_by_sending_late(self):
        pipeline = Pipeline()
        pipeline.through([str.title, str.strip])
        result = pipeline.send('a sample string that is passed through to all pipes.       ') \
            .then_return()
        self.assertEqual('A Sample String That Is Passed Through To All Pipes.', result)

    def test_it_runs_a_pipeline_setup_via_pipe(self):
        pipeline = Pipeline()
        pipeline.pipe([str.title, str.strip])
        result = pipeline.send('a sample string that is passed through to all pipes.       ') \
            .then_return()
        self.assertEqual('A Sample String That Is Passed Through To All Pipes.', result)

    def test_it_bails_early(self):
        pipeline = Pipeline()
        result = pipeline.send('bork') \
            .through([
                lambda x, next: False,
                str.strip
            ]) \
            .then()
        self.assertFalse(result)

    def test_it_bails_in_the_middle(self):
        pipeline = Pipeline()
        result = pipeline.send('bork        ') \
            .through([
                str.strip,
                lambda x, next: x,
                str.title
            ]) \
            .then()
        self.assertEqual('bork', result)

if __name__ == '__main__':
    unittest.main()
