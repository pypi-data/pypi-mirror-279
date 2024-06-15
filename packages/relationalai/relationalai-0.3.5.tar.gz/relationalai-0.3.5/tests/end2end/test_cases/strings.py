import relationalai as rai
from relationalai import std


model = rai.Model(name=globals().get("name", "test_strings"), config=globals().get("config"))
Person = model.Type("Person")
LikePattern = model.Type("LikePattern")

with model.rule():
    Person.add(first="John", last="Coltrane")
    Person.add(first="Miles", last="Davis")
    Person.add(name="Herbie Hancock")
    # Used in the `like` test, which relies on there being exactly one LikePattern instance.
    LikePattern.add(pattern="Mi%")

# Check that 'length' works.
with model.query(tag="length") as select:
    p = Person()
    f_length = std.strings.length(p.last)
    v_length = std.strings.length("Four")
    select(p, p.last, f_length, v_length)

# Check that 'contains' works.
with model.query(tag="contains") as select:
    p = Person()
    with model.union() as u:
        with model.scope():
            std.strings.contains(p.last, "trane")
            u.add(p)
        with model.scope():
            std.strings.contains("SMiles", p.first)
            u.add(p)
    select(p, p.first, p.last)

# Check that 'ends_with' works.
with model.query(tag="ends_with") as select:
    p = Person()
    with model.union() as u:
        with model.scope():
            std.strings.ends_with(p.last, "trane")
            u.add(p)
        with model.scope():
            std.strings.ends_with("SMiles", p.first)
            u.add(p)
    select(u, u.first, u.last)

# Check that 'lowercase' and 'uppercase' work.
with model.query(tag="lowercase") as select:
    p = Person()
    lower = std.strings.lowercase(p.first)
    upper = std.strings.uppercase(p.first)
    select(p, p.first, lower, upper)

# Check that 'join' works.
with model.query(tag="join") as select:
    p = Person()
    name = std.strings.join([p.first, p.last], " ")
    name2 = std.strings.join(["FIRST", p.last], " ")
    name3 = std.strings.join([p.first, "LAST"], " ")
    sep = std.Vars(1)
    sep == ""
    name4 = std.strings.join(["FIRST", "LAST"], sep)
    select(p, p.first, p.last, name, name2, name3, name4)

# Check that concat works:
with model.query(tag="concat") as select:
    p = Person()
    first_name = std.strings.concat(p.first, "")
    last_name = std.strings.concat("", p.last)
    full_name = std.strings.concat(p.first, p.last)
    new_name = std.strings.concat("HEY", "YOU")
    select(p, first_name, last_name, full_name, new_name)

# Check that replace works.
with model.query(tag="replace") as select:
    p = Person(first="John", last="Coltrane")
    s = Person(first="Miles", last="Davis").first
    new1 = std.strings.replace(p.first, old="ohn", new="ohnny")
    new2 = std.strings.replace(p.first, old="ohn", new=s)
    new3 = std.strings.replace(p.first, old=p.first, new=s)
    select(p, p.first, new1, new2, new3)

# Check that 'like' works.
with model.query(tag="like") as select:
    p = Person()
    with model.union() as u:
        with model.scope():
            std.strings.like(p.last, "Col%")
            u.add(p)
        with model.scope():
            pattern = LikePattern()
            std.strings.like(p.first, pattern.pattern)
            u.add(p)
    select(u, u.first, u.last)

# Check that 'regex_match' and 'regex_compile' work.
with model.query(tag="regex_match_and_compile") as select:
    p = Person()
    pattern = std.strings.regex_compile(r"Col.*")
    std.strings.regex_match(p.last, pattern)
    select(p, p.first, p.last)

# Check that 'split' work
with model.query(tag="split") as select:
    p = Person()
    ix, part = std.strings.split(p.name, " ")
    select(ix, part)

# Check that 'split_part' works.
with model.query(tag="split_part") as select:
    p = Person()
    first = std.strings.split_part(p.name, " ", 0)
    last = std.strings.split_part(p.name, " ", 1)
    select(p, p.name, first, last)
