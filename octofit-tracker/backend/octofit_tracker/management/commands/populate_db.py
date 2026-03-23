from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        Team.objects.all().delete()
        User.objects.all().delete()

        # Create users (superheroes)
        marvel_heroes = [
            {'username': 'ironman', 'email': 'ironman@marvel.com', 'first_name': 'Tony', 'last_name': 'Stark'},
            {'username': 'captainamerica', 'email': 'cap@marvel.com', 'first_name': 'Steve', 'last_name': 'Rogers'},
            {'username': 'spiderman', 'email': 'spiderman@marvel.com', 'first_name': 'Peter', 'last_name': 'Parker'},
        ]
        dc_heroes = [
            {'username': 'batman', 'email': 'batman@dc.com', 'first_name': 'Bruce', 'last_name': 'Wayne'},
            {'username': 'superman', 'email': 'superman@dc.com', 'first_name': 'Clark', 'last_name': 'Kent'},
            {'username': 'wonderwoman', 'email': 'wonderwoman@dc.com', 'first_name': 'Diana', 'last_name': 'Prince'},
        ]
        marvel_users = [User.objects.create_user(**hero, password='password') for hero in marvel_heroes]
        dc_users = [User.objects.create_user(**hero, password='password') for hero in dc_heroes]

        # Create teams
        marvel_team = Team.objects.create(name='Marvel')
        dc_team = Team.objects.create(name='DC')
        marvel_team.members.set(marvel_users)
        dc_team.members.set(dc_users)

        # Create workouts
        workout1 = Workout.objects.create(name='Pushups', description='Do 20 pushups')
        workout2 = Workout.objects.create(name='Running', description='Run 5km')
        workout1.suggested_for.set(marvel_users)
        workout2.suggested_for.set(dc_users)

        # Create activities
        Activity.objects.create(user=marvel_users[0], team=marvel_team, type='pushups', duration=10, date=timezone.now())
        Activity.objects.create(user=dc_users[0], team=dc_team, type='running', duration=30, date=timezone.now())

        # Create leaderboards
        Leaderboard.objects.create(team=marvel_team, total_points=100)
        Leaderboard.objects.create(team=dc_team, total_points=120)

        self.stdout.write(self.style.SUCCESS('Test data populated successfully.'))
