import csv
from collections import defaultdict, namedtuple, OrderedDict
from statistics import mean
import operator

GRADUATION_DATA = '2005_2010__Graduation_Outcomes_By_Borough.csv'

HISPANIC = 'Hispanic'
BLACK = 'Black'
ASIAN = 'Asian'
WHITE = 'White'
TOTAL = 'Borough Total'
ELL = 'English Language Learners'
EL_PROFICIENT = 'English Proficient Students'
SPECIAL_ED = 'Special Education'
GENERAL_ED = 'General Education'
FEMALE = 'Female'
MALE = 'Male'

Borough = namedtuple('Borough', 'year rate total')


def filter_and_parse(data=GRADUATION_DATA, filter_val=TOTAL):
    boroughs_dict = defaultdict(list)
    with open(data, encoding='utf-8') as f:
        for line in csv.DictReader(f):
            if line['Demographic'] == filter_val:
                try:
                    borough = str(line['Borough'])
                    year = int(line['Cohort'].replace('Aug 2006', '2007'))
                    rate = float(line['Total Grads - % of cohort'])
                    total = int(line['Total Grads - n'])

                except ValueError:
                    continue

                b = Borough(year=year, rate=rate, total=total)
                boroughs_dict[borough].append(b)
            else:
                continue

    #print(boroughs_dict['Queens'])
    return boroughs_dict


def get_average_gradrate(boroughs):
    '''Filter directors with < MIN_MOVIES and calculate average score'''
    new_dict = {}
    for ny_borough in boroughs:
        year_list = boroughs[ny_borough]
        mean_gradrate = find_grad_rate(year_list)
        new_dict[ny_borough] = mean_gradrate

    #print(new_dict['Queens'])
    return new_dict


def find_grad_rate(borough):
    grad_rates = []
    for year_tup in borough:
        grad_rates.append(year_tup.rate)

    overall_rate = mean(grad_rates)
    return round(overall_rate, 1)

def print_results(boroughs_dict):
    fmt_borough_entry = '{counter}. {borough:<52} {avg}'
    fmt_year_entry = '{year}] {total_students: <50} {rate}'
    sep_line = '-' * 60

    count = 1

    gradrate_dict = get_average_gradrate(boroughs_dict)
    gradrate_list_unsorted = list(gradrate_dict.items())
    gradrate_list = sorted(gradrate_list_unsorted, key=lambda tup: tup[1], reverse=True)

    for i in range(len(gradrate_list)):
        borough_name = str(gradrate_list[i][0])
        borough_rate = gradrate_list[i][1]

        print(fmt_borough_entry.format(counter=count, borough=borough_name, avg=borough_rate))
        print(sep_line)

        tuple_list = sorted(boroughs_dict[borough_name], key=operator.attrgetter('year'), reverse=True)

        for yr in tuple_list:
            print(fmt_year_entry.format(year=yr.year, total_students=yr.total, rate=yr.rate))

        print("\n")
        count += 1


def main():

    filter_input = input("What demographic would you like to see data for?: ")
    boroughs = filter_and_parse(filter_val=filter_input)
    print_results(boroughs)


if __name__ == '__main__':
    main()


