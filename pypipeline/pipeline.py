from typing import Any, Callable, List, Optional, Union
from inspect import signature

class Pipeline:
    """
    A Chain of Responsibility implementation adapted from https://github.com/stellarwp/pipeline
    """
    def __init__(self):
        """
        The constructor.
        """
        self.passable = None
        self.pipes = []
        self.method = 'handle'


    def add_pipe(self, pipes: Union[List, Any]) -> 'Pipeline':
        """
        Alias of `pipe`.

        Args:
            pipes (Union[List, Any]): The pipes to push onto the pipeline.

        Returns:
            Pipeline: Self
        """

        return self.pipe(pipes)

    def carry(self, next_pipe: Callable, current_pipe: Any) -> Callable:
        """
        Get a Closure that represents a slice of the application onion.

        Args:
            next_pipe (Callable): The next pipe to call.
            current_pipe (Any): The current pipe.

        Returns:
            Callable: The callable for the pipe.
        """
        def wrapper(passable):
            print(passable)
            try:
                # Determine how many parameters the current_pipe accepts
                params = signature(current_pipe).parameters
                if callable(current_pipe) and len(params) == 2 and 'next' in params:
                    return current_pipe(passable, next_pipe)
                elif callable(current_pipe):
                    result = current_pipe(passable)
                    return next_pipe(result)
                else:
                    raise TypeError("The pipe must be callable")
            except Exception as e:
                return self.handle_exception(passable, e)
        return wrapper

    def handle_exception(self, passable, exception: Exception):
        """
        Handle the given exception.

        Args:
            passable (Any): The current state of the passable.
            exception (Exception): The exception to raise.

        Raises:
            exception: The exception to raise
        """
        raise exception

    def pipe(self, pipes: Union[List, Any]) -> 'Pipeline':
        """
        Push additional pipes onto the pipeline.

        Args:
            pipes (Union[List, Any]): The pipes to push onto the pipeline.

        Returns:
            Pipeline: Self
        """
        if not isinstance(pipes, list):
            pipes = list(pipes)
        self.pipes.extend(pipes)
        return self

    def prepare_destination(self, destination: Callable) -> Callable:
        """
        Get the final piece of the Closure onion.

        Args:
            destination (Callable): The destination callback.

        Returns:
            Callable: The destination callback.
        """
        def wrapper(passable):
            try:
                return destination(passable)
            except Exception as e:
                return self.handle_exception(passable, e)
        return wrapper

    def run(self, destination: Optional[Callable] = None):
        """
        An alias for `then`.

        Args:
            destination (Optional[Callable], optional): The destination callback. Defaults to None.

        Returns:
            The result of the pipeline.
        """
        return self.then(destination)

    def run_and_return(self):
        """
        An alias for `then_return`

        Returns:
            The result of the pipeline.
        """
        return self.then_return()

    def send(self, passable: Any) -> 'Pipeline':
        """
        Set the value being sent through the pipeline.

        Args:
            passable (Any): The value to pass through the pipeline.

        Returns:
            Pipeline: Self
        """
        self.passable = passable
        return self

    def then(self, destination: Optional[Callable] = None):
        """
        Run the pipeline with a final destination callback.

        Args:
            destination (Optional[Callable], optional): The destination callback. Defaults to None.

        Returns:
            The result of the pipeline.
        """
        if destination is None:
            destination = lambda x: x

        pipeline = self.prepare_destination(destination)

        # We reverse the
        for pipe in reversed(self.pipes):
            pipeline = self.carry(pipeline, pipe)

        return pipeline(self.passable)

    def then_return(self):
        """
        Run the pipeline and return the result.

        Returns:
            The result of the pipeline.
        """
        return self.then()

    def through(self, pipes: Union[List, Any]) -> 'Pipeline':
        """
        Set the array of pipes.

        Args:
            pipes (Union[List, Any]): The pipes to set

        Returns:
            Pipeline: Self
        """
        self.pipes = list(pipes) if isinstance(pipes, list) else list(pipes)
        return self

    def via(self, method: str) -> 'Pipeline':
        """
        Set the method to call on the pipes.

        Args:
            method (str): The method to call on the pipes

        Returns:
            Pipeline: Self
        """
        self.method = method
        return self
