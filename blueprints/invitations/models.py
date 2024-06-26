from app import db


class Invitation(db.Model):
    __tablename__ = 'invitations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                        nullable=False)
    place = db.Column(db.String(80), nullable=False)
    marriage_date = db.Column(db.Date, nullable=False)
    marriage_time = db.Column(db.Time, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(),
                           server_onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Invitation %r>' % self.id
    
class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    invitation_id = db.Column(db.Integer, db.ForeignKey('invitations.id'),
                              nullable=False)
    image = db.Column(db.LargeBinary(length=(2**32)-1),nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    # updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Image %r>' % self.id
    
class Couple(db.Model):
    __tablename__ = 'couples'
    id = db.Column(db.Integer, primary_key=True)
    invitation_id = db.Column(db.Integer, db.ForeignKey('invitations.id'),
                              nullable=False)
    name = db.Column(db.String(80), nullable=False)
    qualification = db.Column(db.String(80), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    groom_bride = db.Column(db.Boolean, nullable=False)
    image = db.Column(db.LargeBinary(length=(2**32)-1), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(),
                           server_onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Couple %r>' % self.id
    
    
class Guest(db.Model):
    __tablename__ = 'guests'
    id = db.Column(db.Integer, primary_key=True)
    invitation_id = db.Column(db.Integer, db.ForeignKey('invitations.id'),
                              nullable=False)
    name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(10),unique=False, nullable=False)
    guests_count = db.Column(db.Integer, nullable=False)
    attending = db.Column(db.String(80), nullable=False)
    message= db.Column(db.String(80), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(),
                           server_onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Guest %r>' % self.id


class Relative(db.Model):
    __tablename__ = 'relatives'
    id = db.Column(db.Integer, primary_key=True)
    couple_id = db.Column(db.Integer, db.ForeignKey('couples.id'),
                              nullable=False)
    name = db.Column(db.String(80), nullable=False)
    relation = db.Column(db.String(80), nullable=False)
    image = db.Column(db.LargeBinary(length=(2**32)-1), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(),
                           server_onupdate=db.func.now())
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Relative %r>' % self.id
