from app import db, login
from flask_login import UserMixin

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    goals = db.relationship("Goal", backref="user", lazy="dynamic")

    def __repr__(self):
        return "<User: {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

parents = db.Table("parents",
    db.Column("parent_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("child_id", db.Integer, db.ForeignKey("user.id"))
)

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    total_time = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    total_rating = db.Column(db.Integer)
    complete = db.Column(db.Boolean, default=False)
    is_master = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    children = db.relationship(
        "Goal", secondary=parents,
        primaryjoin=(parents.c.parent_id == id),
        secondaryjoin=(parents.c.child_id == id),
        backref=db.backref("parents", lazy="dynamic"),
        lazy="dynamic"
    )

    def __repr__(self):
        return "<Goal: {}>".format(self.goal)

    # Relationship tests

    def isParent(self, goal):
        return self.children.filter(parents.c.child_id == goal.id).count() > 0

    def isChild(self, goal):
        return self.parents.filter(parents.c.parent_id == goal.id).count() > 0

    # Relationship creation

    def makeMaster(self):
        self.is_master = True

    def addChild(self, goal):
        if not self.isChild(goal):
            self.children.append(goal)
        else:
            return "'{}' is already connected to '{}'".format(self.goal, goal.goal)

    # Tree listing

    def listTree(self, goal):
        treeList = {goal: goal.children.all()}
        for i in range(len(treeList[goal])):
            treeBranch = {}
            treeBranch
            treeList.append(childGoal)


    # Relationship removal

    def removeRel(self, goal):
        if self.isParent(goal):
            self.children.remove(goal)
        elif self.isChild(goal):
            self.parents.remove(goal)
