# specification for minimum interface for models

class BaseModel:
    def run(self) -> None:
        """Run model and update it."""  # noqa: DAR401
        raise NotImplementedError

    def reset(self) -> None:
        """Reset model to prepare to run again."""  # noqa: DAR401
        raise NotImplementedError
