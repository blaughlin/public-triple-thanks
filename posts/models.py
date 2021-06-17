from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from geopy.geocoders import Nominatim
from localflavor.us.models import USStateField

us_state_abbrev = {
	'Alabama': 'AL',
	'Alaska': 'AK',
	'American Samoa': 'AS',
	'Arizona': 'AZ',
	'Arkansas': 'AR',
	'California': 'CA',
	'Colorado': 'CO',
	'Connecticut': 'CT',
	'Delaware': 'DE',
	'District of Columbia': 'DC',
	'Florida': 'FL',
	'Georgia': 'GA',
	'Guam': 'GU',
	'Hawaii': 'HI',
	'Idaho': 'ID',
	'Illinois': 'IL',
	'Indiana': 'IN',
	'Iowa': 'IA',
	'Kansas': 'KS',
	'Kentucky': 'KY',
	'Louisiana': 'LA',
	'Maine': 'ME',
	'Maryland': 'MD',
	'Massachusetts': 'MA',
	'Michigan': 'MI',
	'Minnesota': 'MN',
	'Mississippi': 'MS',
	'Missouri': 'MO',
	'Montana': 'MT',
	'Nebraska': 'NE',
	'Nevada': 'NV',
	'New Hampshire': 'NH',
	'New Jersey': 'NJ',
	'New Mexico': 'NM',
	'New York': 'NY',
	'North Carolina': 'NC',
	'North Dakota': 'ND',
	'Northern Mariana Islands':'MP',
	'Ohio': 'OH',
	'Oklahoma': 'OK',
	'Oregon': 'OR',
	'Pennsylvania': 'PA',
	'Puerto Rico': 'PR',
	'Rhode Island': 'RI',
	'South Carolina': 'SC',
	'South Dakota': 'SD',
	'Tennessee': 'TN',
	'Texas': 'TX',
	'Utah': 'UT',
	'Vermont': 'VT',
	'Virgin Islands': 'VI',
	'Virginia': 'VA',
	'Washington': 'WA',
	'West Virginia': 'WV',
	'Wisconsin': 'WI',
	'Wyoming': 'WY'
}

abbrev_us_state = dict(map(reversed, us_state_abbrev.items()))

class User(AbstractUser):
	city = models.CharField(max_length=200, default = None, blank= True, null=True)
	state = USStateField(null=True, blank=True)
	#state = models.CharField(max_length=200, default = None, blank= True, null=True)
	zip_code = models.IntegerField(default = None, blank= True, null=True)
	profile_pic = models.ImageField(default= 'default.jpg', blank=True, null=True)
	first_name = models.CharField(max_length=200, default = None, blank= True, null=True)
	last_name = models.CharField(max_length=200, default = None, blank= True, null=True)
	about = models.CharField(max_length=200, default = None, blank= True, null=True)
	lattitude = models.FloatField(default = 0, blank= True, null=True)
	longitude = models.FloatField(default = 0, blank= True, null=True)

	def save(self, *args, **kwargs):
		if self.state != None:
			geolocator = Nominatim(user_agent='pk.eyJ1IjoiYmVybmFyZGxhdWdobGluIiwiYSI6ImNrZ254bzh6bTA4dnUycXBmb2x5MnhhZDEifQ.b1d2QwyPmPBNvzrPbMQ5tQ')
			marker = str(self.city) + ", " + abbrev_us_state[self.state] + "," + str(self.zip_code)
			location = geolocator.geocode(marker)
			self.lattitude = location.latitude
			self.longitude = location.longitude
			super().save(*args, **kwargs)
		else:
			super().save(*args, **kwargs)


class Social(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	followers = models.ManyToManyField(User, related_name='is_following', blank =True)

	def __str__(self):
		return self.user.username

class Post(models.Model):
	post = models.TextField()
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	timestamp = models.DateTimeField(auto_now=False)
	liked = models.ManyToManyField(User, default = None, blank = True, related_name='liked')
	date = models.DateField(auto_now=False)
	private = models.BooleanField(default= False, blank = True)
	def serialize(self):
		return {
			"id": self.id,
			"post": self.post,
			"timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
			"date": self.date.strftime("%b %-d %Y"),
			"liked": [user.post for user in self.liked.all()],
			'private': self.private
			}
	
	@property
	def toalLikes(self):
		return self.liked.all().count()

def saveSocialToUser(sender, instance, created, *args, **kwargs):
	if created:
		social, is_created = Social.objects.get_or_create(user=instance)
		
post_save.connect(saveSocialToUser, sender=User)

LIKE_CHOICES = (
	('Like', 'Like'),
	('Unlinke','Unlike')
	)
 
class Like(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)
	

