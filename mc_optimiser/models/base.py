# specification for minimum interface for models

class BaseModel:
    def run(self) -> None:
        """Run model and update it."""  # noqa: DAR401
        raise NotImplementedError
