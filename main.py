import argparse
import random

from datacenter.models import Schoolkid
from datacenter.models import Chastisement
from datacenter.models import Mark
from datacenter.models import Lesson
from datacenter.models import Commendation

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def create_commendation(schoolkid, subject, year_of_study, group_letter, praises):
	last_lesson = Lesson.objects.filter(year_of_study=year_of_study, group_letter=group_letter,
	                                    subject__title=subject)[-1]

	Commendation.objects.create(subject=subject, schoolkid=schoolkid, teacher=last_lesson.teacher,
	                    text=random.choice(praises), created=last_lesson.date)


def fix_marks(schoolkid):
	bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
	for bad_mark in bad_marks:
		bad_mark.points = 4
		bad_mark.save()

def remove_chastisements(schoolkid):
	bad_chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
	bad_chastisements.delete()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Программа для взлома дневника')

	schoolkid_name = parser.add_argument('-n', '--name', help='Имя ученика', type=str)
	year_of_study = parser.add_argument('-y', '--year', help='Номер класса', type=int)
	group_letter = parser.add_argument('-l', '--letter', help='Буква класса', type=str)
	action = parser.add_argument('-a', '--action', help='''Выберите действие
	                                                    1. Заменить плохие оценки ученика
	                                                    2. Удалить все замечания
	                                                    3. Добавить ученику похвалу''', type=int)
	subject = parser.add_argument('-s', '--subject', help='Предмет', type=str).capitalize()

	try:
		schoolkid = Schoolkid.objects.get(full_name=schoolkid_name, year_of_study=year_of_study,
		                                     group_letter=group_letter)
		if action == 1:
			fix_marks(schoolkid)
		if action == 2:
			remove_chastisements(schoolkid)
		if action == 3 and subject != False:
			with open('praises.txt', 'r') as f:
				praises = f.readlines()
			create_commendation(schoolkid, subject, year_of_study, group_letter)

	except ObjectDoesNotExist:
		print('Такого ученика нет в списке учеников')

	except MultipleObjectsReturned:
		print('Несколько учеников с такими параметрами. Пожалуйста уточните имя ученика')
