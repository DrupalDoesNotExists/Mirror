from pydantic import BaseModel


class Event(BaseModel):
    """ API Event """

    ray_id: str
    code: int = 200
    data: dict

    def format(self) -> str:
        """ Format as event-stream chunk """

        json = self.json()
        return f"data: {json}\n\n"
