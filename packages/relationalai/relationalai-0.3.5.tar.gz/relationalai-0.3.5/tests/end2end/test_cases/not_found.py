#pyright: reportUnusedExpression=false
import relationalai as rai

model = rai.Model(name=globals().get("name", "test_not_found"), config=globals().get("config"))
Invited = model.Type("Invited")
Invite = model.Type("Invite")
Person = model.Type("Person")

with model.rule():
    joe = Person.add(name="Joe", age=74)
    bob = Person.add(name="Bob", age=40)
    jane = Person.add(name="Jane", age=10)

    joe.friends.extend([jane, bob])
    jane.friends.extend([joe, bob])
    bob.friends.add(jane)

    Invited.add(person=joe)

with model.rule():
    p = Person()
    with model.not_found():
        Invited(person=p)

    Invite.add(person=p)

#--------------------------------------------------
# Find all friends that are older than 10 where the
# person doesn't have a friend named Jane.
# This should exlude Joe, since he's friends with Jane
#--------------------------------------------------

with model.query() as select:
    p = Person()
    with model.not_found():
        p.friends.name == "Jane"
    p.friends.age > 8
    res = select(p, p.name, p.age, p.friends.name, p.friends.age)

print(res.results)

#--------------------------------------------------
# Order matters, if we move the condition up, we'll unify
# on friends as well and keep any that don't have a name
# of Jane
#--------------------------------------------------

with model.query() as select:
    p = Person()
    p.friends.age > 8
    with model.not_found():
        p.friends.name == "Jane"
    res = select(p, p.name, p.age, p.friends.name, p.friends.age)

print(res.results)

#--------------------------------------------------
# Find all people who need an invite
#--------------------------------------------------

with model.query() as select:
    res = select(Invite().person.name)
