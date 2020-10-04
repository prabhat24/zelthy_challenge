import datetime
import logging
import random

from django.core.management import BaseCommand

from purchase.models import Purchase, PurchaseStatus

logger = logging.getLogger('django')


def make_avg_7(n, hash):
    if n == 0:
        return
    elif n >= 3:
        choice = random.randint(1, 7)
        hash[choice] += 1
        if choice in range(4, 8):
            hash[10 - (choice - 4)] += 1
            n = n - 2
        if choice in [1, 2, 3]:
            if choice == 1:
                hash[10] += 2
            elif choice == 2:
                hash[10] += 1
                hash[9] += 1
            elif choice == 3:
                hash[9] += 2
            n = n - 3
    elif n >= 2:
        choice = random.randint(4, 7)
        hash[choice] += 1
        hash[10 - (choice - 4)] += 1
        n = n - 2
    elif n == 1:
        hash[7] += 1
        n = n - 1
    return make_avg_7(n, hash)


class Command(BaseCommand):

    def handle(self, *args, **options):
        def populate():
            names = [
                'Puyol',
                'Gerard Piqué',
                'Pedro Rodríguez',
                'Andrés Iniesta',
                'Luis Suárez',
                'Lionel Messi',
                'Neymar',
                'Javier Mascherano',
                'Marc Bartra',
                'Jordi Alba',
            ]
            req_avg = 7
            len_names = len(names)
            records = 50
            hash = [0] * (len_names + 1)

            make_avg_7(records, hash)
            hash = [10 * i for i in hash]
            print(sum(hash))
            for i, name in enumerate(names):
                for _ in range(hash[i + 1]):
                    purchase = create_purchase(name, i + 1)
                    status_choice = ['open', 'verified', 'dispatched', 'delivered', ]
                    rand_int = random.randint(0, 3)
                    st = datetime.datetime.strptime('1/1/2019 5:00 PM', '%d/%m/%Y %I:%M %p')
                    end = datetime.datetime.strptime('31/3/2020 10:00 PM', '%d/%m/%Y %I:%M %p')
                    rand_date = random_date(st, end, rand_int + 1)
                    while rand_int >= 0:
                        create_status(purchase, status=status_choice[rand_int], created_at=rand_date[rand_int])
                        rand_int -= 1

        def create_status(purchase, status, created_at):
            logger.info(
                f"Purchase Status created for purchase_id : {purchase.id}, status : {status}, crated_at : {created_at}")
            s = PurchaseStatus.objects.create(purchase=purchase, status=status, created_at=created_at)
            s.save()
            return s

        def random_date(start, end, length):
            rand_sec = []
            total_sec = int((end - start).total_seconds())
            for _ in range(length):
                sec = random.randint(0, total_sec)
                rand_sec.append(sec)
            rand_sec.sort()
            rand_date = []
            for i in range(length):
                rand_date.append(start + datetime.timedelta(seconds=rand_sec[i]))
            return rand_date

        def create_purchase(name, quantity):
            logger.info(f"Purchase Model created purchase_name : {name}, quantity:{quantity}")
            p = Purchase.objects.create(purchaser_name=name, quantity=quantity)
            p.save()
            return p

        populate()
