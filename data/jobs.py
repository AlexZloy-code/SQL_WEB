import sqlalchemy as sa
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Jobs(SqlAlchemyBase):
    __tablename__ = 'jobs'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    team_leader_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    team_leader = orm.relationship("User")
    job = sa.Column(sa.Text)
    work_size = sa.Column(sa.Integer)
    collaborators = sa.Column(sa.String)
    start_date = sa.Column(sa.Date)
    send_date = sa.Column(sa.Date)
    is_finished = sa.Column(sa.Boolean, default=False)

    def __repr__(self):
        return f"<Jobs {self.id} {self.job} {self.is_finished}>"
