# coding: utf-8

from devourer.systemwide import db


class Person(db.Model):
    __tablename__ = 'Person'

    id = db.Column(db.Integer, primary_key=True)
    createDatetime = db.Column(db.DateTime, nullable=False)
    createPerson_id = db.Column(db.Integer, index=True)
    modifyDatetime = db.Column(db.DateTime, nullable=False)
    modifyPerson_id = db.Column(db.Integer, index=True)
    deleted = db.Column(db.Integer, nullable=False, server_default=u"'0'")
    code = db.Column(db.String(12), nullable=False)
    federalCode = db.Column(db.Unicode(255), nullable=False)
    regionalCode = db.Column(db.String(16), nullable=False)
    lastName = db.Column(db.Unicode(30), nullable=False)
    firstName = db.Column(db.Unicode(30), nullable=False)
    patrName = db.Column(db.Unicode(30), nullable=False)
    post_id = db.Column(db.Integer, index=True)
    speciality_id = db.Column(db.Integer, index=True)
    org_id = db.Column(db.Integer, db.ForeignKey('Organisation.id'), index=True)
    orgStructure_id = db.Column(db.Integer, index=True)
    office = db.Column(db.Unicode(8), nullable=False)
    office2 = db.Column(db.Unicode(8), nullable=False)
    tariffCategory_id = db.Column(db.Integer, index=True)
    finance_id = db.Column(db.Integer, index=True)
    retireDate = db.Column(db.Date, index=True)
    ambPlan = db.Column(db.SmallInteger, nullable=False)
    ambPlan2 = db.Column(db.SmallInteger, nullable=False)
    ambNorm = db.Column(db.SmallInteger, nullable=False)
    homPlan = db.Column(db.SmallInteger, nullable=False)
    homPlan2 = db.Column(db.SmallInteger, nullable=False)
    homNorm = db.Column(db.SmallInteger, nullable=False)
    expPlan = db.Column(db.SmallInteger, nullable=False)
    expNorm = db.Column(db.SmallInteger, nullable=False)
    login = db.Column(db.Unicode(32), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    userProfile_id = db.Column(db.Integer, index=True)
    retired = db.Column(db.Integer, nullable=False)
    birthDate = db.Column(db.Date, nullable=False)
    birthPlace = db.Column(db.String(64), nullable=False)
    sex = db.Column(db.Integer, nullable=False)
    SNILS = db.Column(db.String(11), nullable=False)
    INN = db.Column(db.String(15), nullable=False)
    availableForExternal = db.Column(db.Integer, nullable=False, server_default=u"'1'")
    primaryQuota = db.Column(db.SmallInteger, nullable=False, server_default=u"'50'")
    ownQuota = db.Column(db.SmallInteger, nullable=False, server_default=u"'25'")
    consultancyQuota = db.Column(db.SmallInteger, nullable=False, server_default=u"'25'")
    externalQuota = db.Column(db.SmallInteger, nullable=False, server_default=u"'10'")
    lastAccessibleTimelineDate = db.Column(db.Date)
    timelineAccessibleDays = db.Column(db.Integer, nullable=False, server_default=u"'0'")
    typeTimeLinePerson = db.Column(db.Integer, nullable=False)
    maxOverQueue = db.Column(db.Integer, server_default=u"'0'")
    maxCito = db.Column(db.Integer, server_default=u"'0'")
    quotUnit = db.Column(db.Integer, server_default=u"'0'")
    academicdegree_id = db.Column(db.Integer)
    academicTitle_id = db.Column(db.Integer,)
    uuid_id = db.Column(db.Integer, nullable=False, index=True, server_default=u"'0'")

    @property
    def nameText(self):
        return u' '.join((u'%s %s %s' % (self.lastName, self.firstName, self.patrName)).split())

    @property
    def full_name(self):
        return u'%s%s' % (self.nameText, u' (%s)' % self.speciality if self.speciality else '')

    def __unicode__(self):
        return self.nameText

    def __json__(self):
        return {
            'id': self.id,
            'name': self.nameText,
            'code': self.code,
            'birth_date': self.birthDate,
            'full_name': self.full_name,
            'snils': self.SNILS,
            'inn': self.INN,
        }

    def __int__(self):
        return self.id


class Organisation(db.Model):
    __tablename__ = 'Organisation'

    id = db.Column(db.Integer, primary_key=True)
    createDatetime = db.Column(db.DateTime, nullable=False)
    createPerson_id = db.Column(db.Integer, index=True)
    modifyDatetime = db.Column(db.DateTime, nullable=False)
    modifyPerson_id = db.Column(db.Integer, index=True)
    deleted = db.Column(db.Integer, nullable=False, server_default=u"'0'")
    fullName = db.Column(db.String(255), nullable=False)
    shortName = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False, index=True)
    net_id = db.Column(db.Integer, index=True)
    infisCode = db.Column(db.String(12), nullable=False, index=True)
    obsoleteInfisCode = db.Column(db.String(60), nullable=False)
    OKVED = db.Column(db.String(64), nullable=False, index=True)
    INN = db.Column(db.String(15), nullable=False, index=True)
    KPP = db.Column(db.String(15), nullable=False)
    OGRN = db.Column(db.String(15), nullable=False, index=True)
    OKATO = db.Column(db.String(15), nullable=False)
    OKPF_code = db.Column(db.String(4), nullable=False)
    OKPF_id = db.Column(db.Integer, index=True)
    OKFS_code = db.Column(db.Integer, nullable=False)
    OKFS_id = db.Column(db.Integer, index=True)
    OKPO = db.Column(db.String(15), nullable=False)
    FSS = db.Column(db.String(10), nullable=False)
    region = db.Column(db.String(40), nullable=False)
    Address = db.Column(db.String(255), nullable=False)
    chief = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    accountant = db.Column(db.String(64), nullable=False)
    isInsurer = db.Column(db.Integer, nullable=False, index=True)
    compulsoryServiceStop = db.Column(db.Integer, nullable=False, server_default=u"'0'")
    voluntaryServiceStop = db.Column(db.Integer, nullable=False, server_default=u"'0'")
    area = db.Column(db.String(13), nullable=False)
    isHospital = db.Column(db.Integer, nullable=False, server_default=u"'0'")
    notes = db.Column(db.String, nullable=False)
    head_id = db.Column(db.Integer, index=True)
    miacCode = db.Column(db.String(10), nullable=False)
    isOrganisation = db.Column(db.Integer, nullable=False, server_default=u"'0'")
    uuid_id = db.Column(db.Integer, nullable=False, index=True, server_default=u"'0'")
    isLPU = db.Column(db.Integer, nullable=False, server_default=u"'0'")
    isStationary = db.Column(db.Integer, nullable=False, server_default=u"'0'")
    TFOMSCode = db.Column(db.String(50))

    @property
    def is_insurer(self):
        return bool(self.isInsurer)

    @property
    def is_hospital(self):
        return bool(self.isHospital)

    @property
    def is_lpu(self):
        return bool(self.isLPU)

    @property
    def is_stationary(self):
        return bool(self.isStationary)

    def __unicode__(self):
        return self.fullName

    def __json__(self):
        return {
            'id': self.id,
            'full_name': self.fullName,
            'short_name': self.shortName,
            'title': self.title,
            'infis': self.infisCode,
            'is_insurer': bool(self.isInsurer),
            'is_hospital': bool(self.isHospital),
            'is_lpu': self.is_lpu,
            'is_stationary': self.is_stationary,
            'address': self.Address,
            'phone': self.phone,
            'deleted': self.deleted
        }

    def __int__(self):
        return self.id