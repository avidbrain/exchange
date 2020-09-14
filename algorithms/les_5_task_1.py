"""
1. Пользователь вводит данные о количестве предприятий, их наименования
и прибыль за четыре квартала для каждого предприятия.
Программа должна определить среднюю прибыль (за год для всех предприятий)
и отдельно вывести наименования предприятий, чья прибыль выше среднего
и ниже среднего.

Данные даны ниже в тексте, ручной ввод не реализован ввиду его неудобства.
ООО "Туз червей" 258.69 -158.8 78.87 14.93 3.83 187.9
ООО "Валет треф" -155.84 -203.41 174.06 193.52
АО "Король бубён" -218.21 -183.03 -218.72 430.9
АО "Дама пик" -250.07 221.05 135.42 243.55
ООО "Распасы" 210.56 -256.91 7.77 -14.26 -107.85
Для тренировки deque сделан возможен ввод значений за много кварталов,
при этом для расчетов берутся только последние 4 значения.
"""
from collections import namedtuple, deque, OrderedDict, Counter
import shlex

CompanyRecord = namedtuple('CompanyRecord', 'org, name, profit')


def parse_input(tkn):
    org, name, *qtrs = tkn
    numprofit = map(lambda x: round(float(x) * 1000), deque(qtrs, maxlen=4))
    return CompanyRecord(org, name, sum(numprofit) / 1000)


company_db = OrderedDict()
total_profit = 0
for n, line in enumerate(__doc__.splitlines()):
    tokens = shlex.shlex(line, posix=True)
    tokens.whitespace_split = True
    try:
        company_db[n] = parse_input(tokens)
        total_profit += company_db[n].profit
    except ValueError:
        pass

mean_profit = total_profit / len(company_db)
c = Counter({n: rec.profit - mean_profit for n, rec in company_db.items()})

print(f"Средняя прибыль за год: {mean_profit:.2f}")

print("Компании с прибылью выше средней:")
for n in +c:
    rec = company_db[n]
    print(f"{rec.org:>6} '{rec.name}'")
print("Компании с прибылью ниже средней:")
for n in -c:
    rec = company_db[n]
    print(f"{rec.org:>6} '{rec.name}'")
