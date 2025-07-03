# from modules.testing_module.SignUpTest import SignUp
# from modules.testing_module.TableOrderTest import TableGuest
from test_modules.loginClass import LoginModule  # import the class
from test_modules.config import standard_config
from user_datas import template3_order_user_data  # import template #3 user datas
from polling import Poll
import json


def main_loop(event, context):

    poll_url = "https://orderonline.dev.dsoftonline.com.au"
    template3_url = "https://orderonline.dev.dsoftonline.com.au/ilppyrmonttest/"

    # SETUP POLLING

    main_poll = Poll('main-poll', poll_url, 5.0)
    main_poll.start()

    # SETUP TEST

    test_case = LoginModule(
            name='get_login_page',
            url=template3_url,
            settings=standard_config,
            user_data={
                'email': template3_order_user_data['email'],
                'password': template3_order_user_data['password']
            }
    )

    # RUN TESTS
    test_case.start()

    # RESUME ONCE TESTS FINISH
    test_case.test_thread.join()

    # END POLLING
    main_poll.stop()

    # PUBLISH RESULTS
    print("\n---------- RESULTS ----------")

    test_result = test_case.get_result()
    print_results(test_result, test_case.name)

    return {
        'statusCode': 200,
        'body': json.dumps("Successful")
    }


def print_results(results, name):
    print(f"\n---------- {name.upper()} ----------\n")
    for row in results:
        if row['pass']==True:
            passfail = "PASS"
        else:
            passfail = "FAIL"
        print(f"{row['event']} ({passfail})")


main_loop(None, None)
