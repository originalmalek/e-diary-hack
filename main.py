import argparse
import os
import random
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from datacenter.models import Schoolkid
from datacenter.models import Chastisement
from datacenter.models import Mark
from datacenter.models import Lesson
from datacenter.models import Commendation

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def create_commendation(subject, year_of_study, group_letter):
	last_lesson = Lesson.objects.filter(year_of_study=year_of_study, group_letter=group_letter,
	                                    subject__title=subject)[0]

	Commendation.objects.create(subject=last_lesson.subject, schoolkid=schoolkid, teacher=last_lesson.teacher,
	                            text=random.choice(praises), created=last_lesson.date)


def fix_marks():
	bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
	for bad_mark in bad_marks:
		bad_mark.points = 4
		bad_mark.save()


def remove_chastisements():
	bad_chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
	bad_chastisements.delete()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Программа для взлома дневника')

	parser.add_argument('-n', '--name', help='Имя ученика', type=str)
	parser.add_argument('-y', '--year', help='Номер класса', type=str)
	parser.add_argument('-l', '--letter', help='Буква класса', type=str)
	parser.add_argument('-a', '--action', help='''Выберите действие
	                                                    1. Заменить плохие оценки ученика
	                                                    2. Удалить все замечания
	                                                    3. Добавить ученику похвалу''', type=int)
	parser.add_argument('-s', '--subject', help='Предмет', type=str)
	args = parser.parse_args()

	try:
		schoolkid = Schoolkid.objects.get(full_name__contains=args.name)

		if args.action == 1:
			fix_marks()
			print('Оценки исправлены')

		if args.action == 2:
			remove_chastisements()
			print('Замечания удалены')

		if args.action == 3 and args.subject is not True:
			with open('praises.txt', 'r') as f:
				praises = f.read().splitlines()
			create_commendation(args.subject, args.year, args.letter)
			print('Похвала добавлена')

	except ObjectDoesNotExist:
		print('Такого ученика нет в списке учеников')

	except MultipleObjectsReturned:
		print('Несколько учеников с такими параметрами. Пожалуйста уточните имя ученика')
