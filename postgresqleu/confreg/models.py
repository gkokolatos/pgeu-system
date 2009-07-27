from django.db import models
from django.contrib.auth.models import User

from postgresqleu.countries.models import Country

class PaymentOption(models.Model):
	name = models.CharField(max_length=64, blank=False, null=False)
	infotext = models.TextField(blank=False, null=False)
	url = models.CharField(max_length=1024, null=True, blank=True)
	sortkey = models.IntegerField(null=False, blank=False)

	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['sortkey', ]

class Conference(models.Model):
	urlname = models.CharField(max_length=32, blank=False, null=False, unique=True)
	conferencename = models.CharField(max_length=64, blank=False, null=False)
	startdate = models.DateField(blank=False, null=False)
	enddate = models.DateField(blank=False, null=False)
	location = models.CharField(max_length=128, blank=False, null=False)
	contactaddr = models.EmailField(blank=False,null=False)
	paymentoptions = models.ManyToManyField(PaymentOption)

	def __unicode__(self):
		return self.conferencename

class RegistrationType(models.Model):
	conference = models.ForeignKey(Conference, null=False)
	regtype = models.CharField(max_length=64, null=False, blank=False)
	cost = models.IntegerField(null=False)
	active = models.BooleanField(null=False, blank=False, default=True)

	def __unicode__(self):
		if self.cost == 0:
			return self.regtype
		else:
			return "%s (EUR %s)" % (self.regtype, self.cost)

	def is_registered_type(self):
		# Starts with * means "not attending"
		if self.regtype.startswith('*'): return False
		return True

	@property
	def stringcost(self):
		return str(self.cost)

class ShirtSize(models.Model):
        shirtsize = models.CharField(max_length=32)

        def __unicode__(self):
                return self.shirtsize

class ConferenceRegistration(models.Model):
	conference = models.ForeignKey(Conference, null=False, blank=False)
	regtype = models.ForeignKey(RegistrationType, null=True, blank=True, verbose_name="Registration type")
	attendee = models.ForeignKey(User, null=False, blank=False)
	firstname = models.CharField(max_length=100, null=False, blank=False, verbose_name="First name")
	lastname = models.CharField(max_length=100, null=False, blank=False, verbose_name="Last name")
	email = models.EmailField(null=False, blank=False, verbose_name="E-mail address")
	company = models.CharField(max_length=100, null=False, blank=False, verbose_name="Company")
	address = models.TextField(max_length=200, null=False, blank=False, verbose_name="Address")
	country = models.ForeignKey(Country, null=False, blank=False, verbose_name="Country")
	phone = models.CharField(max_length=100, null=False, blank=True, verbose_name="Phone number")
	shirtsize = models.ForeignKey(ShirtSize, null=False, blank=False, verbose_name="Preferred T-shirt size")
	dietary = models.CharField(max_length=100, null=False, blank=True, verbose_name="Special dietary needs")

	# Admin fields!
	payconfirmedat = models.DateField(null=True, blank=True, verbose_name="Payment confirmed at")
	payconfirmedby = models.CharField(max_length=16, null=True, blank=True, verbose_name="Payment confirmed by")

	# Access from templates requires properties
	@property
	def isregistered(self):
		if not self.regtype: return False
		return self.regtype.is_registered_type()

	@property
	def needspayment(self):
		if not self.regtype: return False
		if self.regtype.cost == 0: return False
		return True

	# For the admin interface (mainly)
	def __unicode__(self):
		return "%s: %s %s <%s>" % (self.conference, self.firstname, self.lastname, self.email)
