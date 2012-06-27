import bank_data.run
import random
import veritable

API = veritable.connect()


def test_bank_data():
    bank_data.run.TABLE_ID = 'bank-data-example_'+str(random.randint(0, 100000000))
    bank_data.run.main()
    API.delete_table(bank_data.run.TABLE_ID)



