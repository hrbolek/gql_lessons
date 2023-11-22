import strawberry
import typing
import asyncio
import uuid
from typing import Annotated, List

def getLoaders(info):
    return info.context['all']

PlannedLessonGQLModel = Annotated["PlannedLessonGQLModel", strawberry.lazy(".PlannedLessonGQLModel")]
PlanGQLModel = Annotated["PlanGQLModel", strawberry.lazy(".PlanGQLModel")]

@strawberry.federation.type(extend=True, keys=["id"])
class AcSemesterGQLModel:

    id: uuid.UUID = strawberry.federation.field(external=True)

    @classmethod
    async def resolve_reference(cls, id: uuid.UUID):
        return AcSemesterGQLModel(id=id)
    
    @strawberry.field(description="""Plans""")
    async def plans(self, info: strawberry.types.Info) -> List["PlanGQLModel"]:
        loader = getLoaders(info).psps
        result = await loader.filter_by(semester_id=self.id)
        return result