from pypipeline.pipeline import Pipeline
import unittest

class TestPipeline(unittest.TestCase):


    def test_it_runs_a_pipeline_with_one_callable(self):
        pipeline = Pipeline()
        result = pipeline.send('hello       ') \
            .through([str.strip]) \
            .then_return()
        self.assertEqual('hello', result)

    def test_it_runs_a_pipeline_with_callables(self):
        pipeline = Pipeline()
        result = pipeline.send('hello world       ') \
            .through([str.title, str.strip]) \
            .then_return()
        self.assertEqual('Hello World', result)

    def test_it_runs_a_pipeline_with_callables_and_executes_the_destination(self):
        pipeline = Pipeline()
        result = pipeline.send('hello world       ') \
            .through([str.title, str.strip]) \
            .then(lambda x: x.replace('Hello', 'Goodbye'))
        self.assertEqual('Goodbye World', result)

    def test_it_runs_a_pipeline_with_callables_and_closures(self):
        pipeline = Pipeline()
        result = pipeline.send('hello world       ') \
            .through([
                lambda x, next_pipe: next_pipe(x.replace('hello', 'goodbye')),
                str.title,
                str.strip
            ]) \
            .then_return()
        self.assertEqual('Goodbye World', result)

    def test_it_runs_a_pipeline_with_closures(self):
        pipeline = Pipeline()
        result = pipeline.send('hello world') \
            .through([
                lambda x, next_pipe: next_pipe(x.title()),
                lambda x, next_pipe: next_pipe(x.replace('Hello', 'Goodbye'))
            ]) \
            .then_return()
        self.assertEqual('Goodbye World', result)

    def test_it_runs_a_pipeline_with_custom_pipes(self):
        def custom_pipe(passable, next_pipe):
            passable = passable.replace('Hello', 'Goodbye')
            return next_pipe(passable)

        pipeline = Pipeline()
        result = pipeline.send('   hello world    ') \
            .through([
                lambda x, next_pipe: next_pipe(x.title()),
                str.strip,
                custom_pipe
            ]) \
            .then_return()
        self.assertEqual('Goodbye World', result)

    def test_it_runs_a_pipeline_with_classes(self):
        class TitlePipe:
            def handle(self, passable, next_pipe):
                return next_pipe(passable.title())

        pipeline = Pipeline()
        result = pipeline.send('   hello world    ') \
            .through([
                TitlePipe(),
                str.strip
            ]) \
            .then_return()
        self.assertEqual('Hello World', result)

    def test_it_runs_a_pipeline_with_classes_and_custom_handler(self):
        class TitlePipe:
            def execute(self, passable, next_pipe):
                return next_pipe(passable.title())

        pipeline = Pipeline()
        result = pipeline.send('   hello world    ') \
            .via('execute') \
            .through([
                TitlePipe(),
                str.strip
            ]) \
            .then_return()
        self.assertEqual('Hello World', result)

    def test_it_runs_a_pipeline_by_sending_late(self):
        pipeline = Pipeline()
        pipeline.through([str.title, str.strip])
        result = pipeline.send('hello       ') \
            .then_return()
        self.assertEqual('Hello', result)

    def test_it_runs_a_pipeline_setup_via_pipe(self):
        pipeline = Pipeline()
        pipeline.pipe([str.title, str.strip])
        result = pipeline.send('hello       ') \
            .then_return()
        self.assertEqual('Hello', result)

    def test_it_bails_early(self):
        pipeline = Pipeline()
        result = pipeline.send('bork') \
            .through([
                lambda x, next_pipe: False,
                str.strip
            ]) \
            .then()
        self.assertFalse(result)

    def test_it_bails_in_the_middle(self):
        pipeline = Pipeline()
        result = pipeline.send('bork        ') \
            .through([
                str.strip,
                lambda x, next_pipe: x,
                str.title
            ]) \
            .then()
        self.assertEqual('bork', result)

if __name__ == '__main__':
    unittest.main()
