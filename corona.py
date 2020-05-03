import random
import matplotlib.pyplot as plt
import PySimpleGUI as sg
from datetime import datetime
from datetime import date
from sys import exit

# from json import
# from os import path
# import copy

# Header Start
About = '''
Corona Virus Model
Author: Robert Leyendecker
Version: .1
Date: April 11, 2020
Menus: PySimpleGUI
Plots: matplotlib
Windows Exe: Pyinstaller

Corona Virus Instructional Project
Author: Robert Leyendecker, Austin, TX
First Version: Apr 11, 2020
(c) 2020, Robert Leyendecker

This program is intended to explore the political choices available to confront a pandemic.
Each choice involves a policy decision that has life and death consequences. 
- Do we spend tax money on testing or do we give tax breaks to the rich in an election year?
- Do we focus on early containment or do nothing in the hope that it will just go away?
- How many deaths will occur as a result of our decision?

This code may be modified and distributed freely as long as this header is included at the top
of this code and any derived code
'''
# Header End

fout = 0


def event_day(d):
    end = date.today()
    start = datetime.strptime(d, "%m/%d/%Y").date()
    return abs(end - start).days


def pretty(d, indent=0, buf=''):
    for key, value in d.items():
        buf += ' ' * indent + str(key) + ':'
        if isinstance(value, dict):
            buf += pretty(value, indent + 1, '\n')
            if not indent:
                buf += '\n'
        else:
            buf += ' ' + str(value) + '\n'
    return buf


def outp(s):
    # print(s)
    return


def outpf(s):
    outp(s)
    fout.write("{0}\n".format(s))


def outf(s):
    fout.write("{0}\n".format(s))


def get_defaults():
    defs = {
        'Outside Lockdown': {
            'response_model': {'val': 'Political (USA)', 'tip': 'How will we prioritize the response?',
                               'drop': ['Political (USA)', 'Slow Medical', 'Fast Medical', 'Aggressive (Taiwan)', 'No Response']},
            'percent_sick_traced': {'val': .1, 'tip': 'From the symptomatic population, how many contacts can be traced and isolated?'},
            'allow_testing': {'val': False, 'tip': 'Will we routinely test sick people?'},
            'allow_learning': {'val': False, 'tip': 'Will update our response protocol later?'},
            'allow_lockdown': {'val': False, 'tip': 'Will we lockdown population based on trend data?'},
            'show_virus': {'val': False, 'tip': 'Show replication rate, scale factors, event onset, etc'},
            'show_health_care': {'val': False, 'tip': 'Show health care parameters'},
            'plot_cumulative_cases': {'val': False, 'tip': 'Are we flattening the curve?'},
            'plot_new_cases': {'val': False, 'tip': 'Plot the new cases being discovered'},
            'plot_hospital_beds': {'val': False, 'tip': 'Plot the number of hospital beds being used'},
            'meta': {
                'title': 'Political Parameters',
                'children': {
                    'Testing Parameters': 'allow_testing',
                    'Lessons Learned': 'allow_learning',
                    'Lockdown Parameters': 'allow_lockdown',
                    'Virus Parameters': 'show_virus',
                    'Health Care': 'show_health_care',
                }
            }
        },
        'Lockdown Parameters': {
            'days_of_denial': {'val': 60, 'tip': 'The minimum number of days we wait before invoking lockdown.'},
            'percent_isolated': {'val': .75, 'tip': 'Percentage of people who isolate themselves during lockdown.'},
            'days_of_trend_needed': {'val': 30, 'tip': 'Days of trending data are needed before changing lockdwn state.'},
            'days_min_duration': {'val': 30, 'tip': 'Minimum  number of days for a lockdown.'},
            'case_threshold': {'val': 2500, 'tip': 'Maximum number of cases to end lockdown.'},
            'forced_ending': {'val': False, 'tip': 'Do we end lockdown regardless of of the trend or number of cases?'},
            'attack': {'val': .97, 'tip': 'How fast do we enter lockdown (higher is slower)?'},
            'decay': {'val': .97, 'tip': 'How fast do we exit lockdown (higher is slower)?'},
            'meta': {
                'parent': 'Outside Lockdown'
            }
        },
        'Testing Parameters': {
            'days_to_deploy': {'val': 0, 'tip': 'Days before deploying testing?'},
            'days_before_result': {'val': 5, 'tip': 'Days before test results.'},
            'percent_sick_tested': {'val': .001, 'tip': 'Percent of people showing symptoms being tested.'},
            'percent_accuracy': {'val': .8, 'tip': 'Percentage of accurate positive test results.'},
            'percent_pos_traced': {'val': .25, 'tip': 'Percentage of contacts from positive test case that can be isolated?'},
            'meta': {
                'parent': 'Outside Lockdown'
            }
        },
        'Lessons Learned': {
            'days_to_deploy': {'val': 0, 'tip': 'Days before deploying any lessons learned.'},
            'percent_sick_traced': {'val': .2, 'tip': 'From people who are sick, how many contacts can we isolate?'},
            'allow_lockdown': {'val': True, 'tip': 'Can we lockdown as part of lessons learned?'},
            'allow_testing': {'val': False, 'tip': 'Can we test as part of lessons learned?'},
            'meta': {
                'children': {
                    'Testing Lessons Learned': 'allow_testing',
                    'Lockdown Lessons Learned': 'allow_lockdown'
                },
                'parent': 'Outside Lockdown'
            }
        },
        'Lockdown Lessons Learned': {
            'days_of_denial': {'val': 0, 'tip': 'Minimum number of days we wait before invoking lockdown after lessons learned.'},
            'percent_isolated': {'val': .75, 'tip': 'Percentage of people observing isolation during lockdown after lessons learned?'},
            'days_of_trend_needed': {'val': 14, 'tip': 'How many days of infection trend data needed to change state of lockdown?'},
            'forced_ending': {'val': False, 'tip': 'Do we force lockdown to end regardless of case load or trend?'},
            'meta': {
                'parent': 'Lessons Learned'
            }
        },
        'Testing Lessons Learned': {
            'days_before_result': {'val': 3, 'tip': 'Days before test result known'},
            'percent_sick_tested': {'val': .001, 'tip': 'Number of people with symptoms tested'},
            'percent_accuracy': {'val': .8, 'tip': 'Percent of positive tests correctly identified'},
            'percent_pos_traced': {'val': .25, 'tip': 'Percent of contacts isolated when someone tests positive'},
            'meta': {
                'parent': 'Lessons Learned'
            }
        },
        'Virus Parameters': {
            'date_start': {'val': '1/31/2020', 'tip': 'Not recommended to change.'},
            'days_before_symptoms': {'val': 5, 'tip': 'Not recommended to change.'},
            'days_before_free': {'val': 21, 'tip': 'Not recommended to change.'},
            'percent_with_symptoms': {'val': .8, 'tip': 'Not recommended to change.'},
            'percent_with_mild_symptoms': {'val': .5, 'tip': 'Not recommended to change.'},
            'r0': {'val': 1.65, 'tip': 'Not recommended to change.'},
            'r0_random': {'val': False, 'tip': 'Not recommended to change.'},
            'r0_jitter': {'val': .005, 'tip': 'Not recommended to change.'},
            'r_range': {'val': .5, 'tip': 'Not recommended to change.'},
            'r_offset': {'val': .25, 'tip': 'Not recommended to change.'},
            'meta': {
                'parent': 'Outside Lockdown'
            }
        },
        'Health Care': {
            'percent_dr_visit': {'val': .2, 'tip': 'How many symptomatic people visit doctor''s office?'},
            'percent_er_visit': {'val': .05, 'tip': 'How many symptomatic people visit the ER?'},
            'percent_symptom_admit': {'val': .2, 'tip': 'How many symptomatic people are admitted to hospital?'},
            'days_before_admit': {'val': 10, 'tip': 'How many days before symptomatic people enter hospital?'},
            'days_admit_duration': {'val': 6, 'tip': 'How many days do people spend in hospital?'},
            'percent_symptom_death': {'val': .055, 'tip': 'How many symptomatic people die?'},
            'cost_admit_per_day': {'val': 8000, 'tip': 'What is daily cost of hospital stay?'},
            'cost_dr_visit': {'val': 400, 'tip': 'What is cost of DR office visit?'},
            'cost_er_visit': {'val': 5000, 'tip': 'What is cost of ER visit?'},
            'cost_death': {'val': 10000, 'tip': 'What is cost of death?'},
            'meta': {
                'parent': 'Outside Lockdown'
            }
        }
    }

    defs['Testing Parameters']['days_to_deploy']['val'] = defs['Lockdown Parameters']['days_of_denial']['val'] * 2
    defs['Lessons Learned']['days_to_deploy']['val'] = defs['Lockdown Parameters']['days_of_denial']['val'] * 2

    return defs


def set_model(model):

    defs = get_defaults()

    default = defs['Outside Lockdown']
    ld = defs['Lockdown Parameters']
    test = defs['Testing Parameters']
    ll = defs['Lessons Learned']
    ll_test = defs['Testing Lessons Learned']
    ll_ld = defs['Lockdown Lessons Learned']
    health = defs['Health Care']

    default['response_model']['val'] = model

    if model == 'Political (USA)':
        default['allow_learning']['val'] = True
        default['allow_lockdown']['val'] = True
        ld['forced_ending']['val'] = True
        ld['attack']['val'] = .98
        ll['allow_testing']['val'] = True
        ll_ld['forced_ending']['val'] = True

    elif model == 'Slow Medical':
        default['allow_learning']['val'] = True
        default['allow_lockdown']['val'] = True
        ld['days_of_denial']['val'] = 60
        ll['allow_testing']['val'] = True
        ll['days_to_deploy']['val'] = 90
        ll_test['percent_sick_tested']['val'] = .005

    elif model == 'Fast Medical':
        default['allow_learning']['val'] = True
        default['allow_lockdown']['val'] = True
        ld['days_of_denial']['val'] = 30
        ll['allow_testing']['val'] = True
        ll['days_to_deploy']['val'] = 60
        ll_test['percent_sick_tested']['val'] = .01

    elif model == 'Aggressive (Taiwan)':
        default['percent_sick_traced']['val'] = .2
        default['allow_learning']['val'] = False
        default['allow_testing']['val'] = True
        default['allow_lockdown']['val'] = True
        ld['days_of_denial']['val'] = 14
        ld['percent_isolated']['val'] = .8
        ld['days_of_trend_needed']['val'] = 7
        test['days_to_deploy']['val'] = 21
        test['days_before_result']['val'] = 2
        test['percent_pos_traced']['val'] = .3
        health['percent_symptom_death']['val'] = .03

    return defs


def get_keys(dct, value):
    return [key for key in dct if (dct[key] == value)]


def run_sim(parms):
    global fout

    fout = open("corona_early_cure.csv", "w+")

    default = parms['Outside Lockdown']
    ld = parms['Lockdown Parameters']
    test = parms['Testing Parameters']
    care = parms['Health Care']
    virus = parms['Virus Parameters']
    ll = parms['Lessons Learned']
    ll_test = parms['Testing Lessons Learned']
    ll_ld = parms['Lockdown Lessons Learned']
    plots = default

    # percent of we find to isolate after contact with person showing symptoms
    response_model = default['response_model']['val']

    # percent of we find to isolate after contact with person showing symptoms
    percent_sick_traced = default['percent_sick_traced']['val']

    # is testing enabled?
    test_allowed = default['allow_testing']['val']

    # is lessons learned enabled?
    ll_allowed = default['allow_learning']['val']

    # is lockdown enabled
    ld_allowed = default['allow_lockdown']['val']

    # forced ending regardless of active cases?
    ld_forced_ending = ld['forced_ending']['val']

    # delay to begin lockdown measures
    ld_days_of_denial = ld['days_of_denial']['val']

    # percentage of people observing lockdown
    ld_percent_isolated = ld['percent_isolated']['val']

    # how many consecutive days of increases before lockdown started
    ld_days_of_trend_needed = ld['days_of_trend_needed']['val']

    # how many consecutive days of decreases before lockdown lifted
    ld_days_duration = ld['days_min_duration']['val']

    # number of cases must be less than this to lift
    ld_case_threshold = ld['case_threshold']['val']

    # alpha to start lockdown
    w1 = ld['attack']['val']

    # alpha to lift lockdown
    w2 = ld['decay']['val']

    # days to deploy testing
    test_days_to_deploy = test['days_to_deploy']['val']

    # days before test results
    test_days_before_result = test['days_before_result']['val']

    # percent of carriers tested before symptoms
    test_percent_sick_tested = test['percent_sick_tested']['val']

    # percent who correctly test positive
    test_percent_accuracy = test['percent_accuracy']['val']

    # percent of we find to isolate after contact with person who has pos test
    test_percent_pos_traced = test['percent_pos_traced']['val']

    # after first lockdown, improved tracing and detection
    ll_percent_sick_traced = ll['percent_sick_traced']['val']
    ll_days_to_deploy = ll['days_to_deploy']['val']
    ll_ld_allowed = ll['allow_lockdown']['val']
    ll_ld_days_of_denial = ll_ld['days_of_denial']['val']
    ll_ld_days_of_trend_needed = ll_ld['days_of_trend_needed']['val']
    ll_ld_percent_isolated = ll_ld['percent_isolated']['val']
    ll_ld_forced_ending = ll_ld['forced_ending']['val']
    ll_test_allowed = ll['allow_testing']['val']
    ll_test_percent_pos_traced = ll_test['percent_pos_traced']['val']
    ll_test_days_before_result = ll_test['days_before_result']['val']
    ll_test_percent_accuracy = ll_test['percent_accuracy']['val']
    ll_test_percent_sick_tested = ll_test['percent_sick_tested']['val']

    pbuf1 = ""
    pbuf1 += "Baseline Response: {}\n".format(response_model)
    pbuf1 += "  Percent Sick Traced: {0:0.4f}\n".format(percent_sick_traced)
    if not ld_allowed:
        pbuf1 += "  No Lockdown\n"
    else:
        pbuf1 += "  Denial Before Lockdown: {0}\n".format(ld_days_of_denial)
        pbuf1 += "  Lockdown Duration: {0}\n".format(ld_days_duration)
        pbuf1 += "  Days Trend Before Change: {0}\n".format(ld_days_of_trend_needed)
        pbuf1 += "  Isolated: {0:0.4f}\n".format(ld_percent_isolated)
        pbuf1 += "  Forced Ending: {0}\n".format(ld_forced_ending)
        pbuf1 += "  Begin/End Case Threshold: {0}\n".format(ld_case_threshold)
        pbuf1 += "  Attack/Decay: {0:.4f} / {1:.4f}\n".format(w1, w2)
    if not test_allowed:
        pbuf1 += "  No Initial Testing\n"
    else:
        pbuf1 += "  Days to Deploy Testing: {}\n".format(test_days_to_deploy)
        pbuf1 += "  Test Accuracy: {0}\n".format(test_percent_accuracy)
        pbuf1 += "  Tested {0},  Result Wait {1}\n".format(test_percent_sick_tested, test_days_before_result)
        pbuf1 += "  Isolated, Adj by Wait: {0:0.4f}\n".format(test_percent_pos_traced / test_days_before_result)

    if ll_allowed:
        pbuf1 += "\nDays to Lessons Learned: {0}\n".format(ll_days_to_deploy)
        pbuf1 += "  Sick Traced: {}\n".format(ll_percent_sick_traced)
        if not ll_ld_allowed:
            pbuf1 += "  No Lockdown\n"
        else:
            pbuf1 += "  Days Denial: {}\n".format(ll_ld_days_of_denial)
            pbuf1 += "  Days Trend Before Change: {}\n".format(ll_ld_days_of_trend_needed)
            pbuf1 += "  Isolated: {0}\n".format(ll_ld_percent_isolated)
            pbuf1 += "  Forced Ending: {0}\n".format(ll_ld_forced_ending)

        if not ll_test_allowed:
            pbuf1 += "  No Testing\n"
        else:
            pbuf1 += "  Test Accuracy: {0}\n".format(ll_test_percent_accuracy)
            pbuf1 += "  Tested {0},  Result Wait {1}\n".format(ll_test_percent_sick_tested, ll_test_days_before_result)
            pbuf1 += "  Isolated, Adj by Wait: {0:0.4f}\n".format(ll_test_percent_pos_traced / ll_test_days_before_result)
    else:
        pbuf1 += "  No Lessons Learned\n"

    # ###############  things we cannot control  ###############

    # days before detection (symptoms, test result)
    days_before_symptoms = virus['days_before_symptoms']['val']

    # days until no longer contagious
    days_before_free = virus['days_before_free']['val']

    # percent who show symptoms
    percent_with_symptoms = virus['percent_with_symptoms']['val']

    # percent who get test for mild symptoms, wait for test results
    # may not isolate or contact trace
    percent_with_mild_symptoms = .5

    # percent who have more severe symptoms, no test needed
    # to suspect case, will self-isolate, will contact trace
    # no waiting for results
    percent_with_sev_symptoms = 1 - percent_with_mild_symptoms

    # percent of all who show systems and end up in hospital
    percent_with_hosp_symptoms = .2

    # infection rate without symptoms
    r0 = virus['r0']['val']
    r0_random = virus['r0_random']['val']
    r0_jitter = virus['r0_jitter']['val']

    # r_offset + r_range * x
    r_offset = virus['r_offset']['val']
    r_range = virus['r_range']['val']
    date_start = virus['date_start']['val']

    pbuf2 = ""
    pbuf2 += "\nVirus Parameters\n"
    pbuf2 += "  Start Date (m/d/y): {}\n".format(date_start)
    pbuf2 += "  Infections Per Day: {0}\n".format(r0)
    pbuf2 += "  Percent With Symptoms: {0}\n".format(percent_with_symptoms)
    pbuf2 += "  Days Before Free: {0}\n".format(days_before_free)
    pbuf2 += "  USA Based R Scaling: {0} + {1} * x\n".format(r_offset, r_range)
    pbuf2 += "  Random: {0}, Jitter: {1}\n".format(r0_random, r0_jitter)

    # ###################  health care costs #################

    # percent with symptoms visit dr
    percent_dr_visit = care['percent_dr_visit']['val']

    # percent with symptoms visit er
    percent_er_visit = care['percent_er_visit']['val']

    # percent with symptoms needing hospital
    percent_symptom_admit = care['percent_symptom_admit']['val']

    # days before admitted after exposure
    days_before_admit = care['days_before_admit']['val']

    # hospital days stay
    days_admit_duration = care['days_admit_duration']['val']

    # dr office visit
    cost_dr_visit = care['cost_dr_visit']['val']

    # hosp visit
    cost_admit_per_day = care['cost_admit_per_day']['val']

    # er visit, then home
    cost_er_visit = care['cost_er_visit']['val']

    # how many with symptoms will die
    percent_symptom_dead = care['percent_symptom_death']['val']

    # how much death costs
    cost_death = care['cost_death']['val']

    pbuf3 = ""
    pbuf3 += "\nHealth Care\n"
    pbuf3 += "  Days Before Hospital Admit: {0}\n".format(days_before_admit)
    pbuf3 += "  Days in Hospital: {0}\n".format(days_admit_duration)
    pbuf3 += "  Visit Dr Office: {0}, ${1} per visit\n".format(percent_dr_visit, cost_dr_visit)
    pbuf3 += "  Visit ER: {0}, ${1} per visit\n".format(percent_er_visit, cost_er_visit)
    pbuf3 += "  Hospital: {0}, ${1} per day\n".format(percent_symptom_admit, cost_admit_per_day)
    pbuf3 += "  Dead: {0}, ${1} per death\n".format(percent_symptom_dead, cost_death)

    #############################################################

    public_list = list()
    hosp_list = list()
    tot_list = list()
    iso_list = list()
    ld_endx = list()
    ld_endy = list()
    ld_startx = list()
    ld_starty = list()
    intro_list = list()

    def_trace = r_offset + percent_sick_traced * r_range
    test_trace = (r_offset + test_percent_pos_traced * r_range) / test_days_before_result

    h = 0
    sick_cnt = 0
    itot = 1
    ld = 0
    ld_val = 0
    delta_cnt = 0
    ld_check = ld_days_of_denial
    last_stat = 0
    er_visit = 0
    dr_visit = 0
    hosp_admit = 0
    death_visit = 0
    iso = 0
    public = 1
    iso_cnt = 0
    ll_enabled = 0
    ll_val = 0
    end_it = 0
    end_cnt = 0
    tot_days = 0
    test_enabled = False
    icum = 0
    intro = 0
    ev_day = event_day(date_start)

    plot_itot = list()
    plot_x = list()
    plot_dead = list()
    plot_iso = list()
    plot_hosp = list()
    plot_icum = list()
    plot_inew = list()

    test_time = test_days_to_deploy + days_before_symptoms + test_days_before_result

    if not (test_percent_sick_tested and test_percent_accuracy and test_percent_pos_traced):
        test_allowed = False

    if not (ll_test_percent_sick_tested and ll_test_percent_accuracy and ll_test_percent_pos_traced):
        ll_test_allowed = False

    outf("end of day, infected, isolated, hospitalized, lockdown active")

    for i in range(0, 730):

        outp(
            "end day: {0:4d}, infected: {1:10.2f}, hospital: {2:10.2f}, lockdown: {3:d}, r0: {4:1.3f}, iso: {5:10.2f}, public: {6:10.2f}, ld_cnt: {7:d}, trace: {8:0.4f} / {9:0.4f}".format(
            i + 1, itot, h, delta_cnt, r0, iso_cnt, public, ld, test_trace, def_trace))

        outf("{0:4d}, {1:10.2f}, {2:10.2f}, {3:10.2f}, {4:10.2f}".format(i + 1, itot, iso_cnt, h, ld_val))

        # accumulate infections
        itot += public + iso

        # save this for removal later after no longer infectious
        tot_list.append(public + iso)
        icum += public + iso

        # we count isolated per day
        iso_cnt += iso
        iso_list.append(iso)
        iso = 0

        # save number of new infections no symptoms
        public_list.append(public)

        # our plot lists
        plot_x.append(i+1)
        plot_itot.append(itot)
        plot_icum.append(icum)
        plot_iso.append(iso)
        plot_dead.append(death_visit)
        plot_hosp.append(h)
        plot_inew.append(public + iso)

        if not test_enabled and test_allowed and i >= test_time - 1:
            test_enabled = True

        if not ll_enabled and ll_allowed and i >= ll_days_to_deploy - 1:
            outp("========== deploy lessons learned {} {}==========".format(i, itot))

            test_trace = (r_offset + test_percent_pos_traced * r_range) / ll_test_days_before_result
            percent_sick_traced = ll_percent_sick_traced

            if ll_ld_allowed:
                ld_check += ll_ld_days_of_denial - ld_days_of_denial
                ld_days_of_denial = ll_ld_days_of_denial
                ld_days_of_trend_needed = ll_ld_days_of_trend_needed
                ld_percent_isolated = ll_ld_percent_isolated
                ld_forced_ending = ll_ld_forced_ending

            if ll_test_allowed:
                test_percent_pos_traced = ll_test_percent_pos_traced
                test_percent_sick_tested = ll_test_percent_sick_tested
                test_percent_accuracy = ll_test_percent_accuracy
                test_time = ll_days_to_deploy + days_before_symptoms + ll_test_days_before_result
                test_enabled = True

            if ld:
                def_trace = r_offset + ld_percent_isolated * r_range
            else:
                def_trace = r_offset + percent_sick_traced * r_range

            ll_val = itot
            ll_enabled = 1

        # introduced cases
        if not ld:
            intro += 1
            intro_list.append(1)
        if i >= days_before_free and intro_list:
            intro -= intro_list.pop(0)

        if i >= days_before_symptoms - 1:

            # People who self-isolate due to more severe symptoms
            # that clearly indicate infection. we assume
            # some contacts will be traced and found and isolated.
            # even though they may go to dr, the symptoms clearly
            # indicate suspected case, test may be pos later, but
            # isolation begins now.
            sick_cnt = public * percent_with_symptoms * percent_with_sev_symptoms

            # find out how many we isolate
            # scale to match country data
            if ld:
                x = r_offset + ld_percent_isolated * r_range
                def_trace = w1 * def_trace + (1 - w1) * x
            else:
                x = r_offset + percent_sick_traced * r_range
                def_trace = w2 * def_trace + (1 - w2) * x

            # number of public traced and isolated
            iso += public * def_trace

            # number of public not isolated
            public *= (1 - def_trace)

            # public += .5

            # put back on list
            public_list.insert(0, public)

        if test_enabled and i >= test_time - 1:

            # find out who is testing positive - we only test people showing symptoms
            # this emulates a person with milder symptoms who goes to dr and gets routine test
            pos = public * test_percent_sick_tested * test_percent_accuracy * percent_with_symptoms * percent_with_mild_symptoms
            iso += pos
            sick_cnt += pos
            public -= pos

            # random testing
            # pos = public * .001
            # iso += pos
            # sick_cnt += pos
            # public -= pos

            # number of public traced and isolated
            pos = public * test_trace
            iso += pos
            public -= pos


            # number of public not traced
            # public *= (1 - test_trace)

        # here try to count hospital beds and deaths
        # and add up total costs
        if i >= days_before_admit - 1:

            # number who will die
            # dead_cnt = sick * percent_symptom_dead
            # death_visit += dead_cnt
            death_visit = icum * percent_symptom_dead * percent_with_symptoms

            # er visits
            er_visit += sick_cnt * percent_er_visit

            # dr visits
            dr_visit += sick_cnt * percent_dr_visit

            # add in those on iso list
            admit = sick_cnt * percent_symptom_admit

            # add to hospital list
            hosp_list.append(admit)

            # accumulate hospital admits
            h += admit
            hosp_admit += admit

        if i >= days_before_admit + days_admit_duration - 1:
            h -= hosp_list.pop(0) if hosp_list else 0

        if i >= days_before_free - 1:
            itot -= tot_list.pop(0)
            iso_cnt -= iso_list.pop(0)

        if r0_random:
            r0 = random.uniform(r0-r0_jitter, r0+r0_jitter)

        public *= r0

        # can we emulate introduced infections from outside?
        #iso += 1

        stat = itot
        # print("i {}, r {}, ld {}, ll {}, cnt {}, inc {}, dd {}, st {}, lc {}".format(i, r0, ld, ll_enabled, delta_cnt, ld_days_of_trend_needed, ld_days_of_denial, stat, last_stat))

        if ld_allowed:
            if not ld:
                delta_cnt = delta_cnt + 1 if stat > last_stat else 0
            else:
                delta_cnt = delta_cnt - 1 if stat < last_stat else 0

            last_stat = stat
            if i >= ld_check and not ld:
                if delta_cnt >= ld_days_of_trend_needed:
                    ld = 1
                    delta_cnt = 0
                    ld_val = stat
                    ld_check = ld_days_duration + i
                    ld_startx.append(i+1)
                    ld_starty.append(itot)
                    outp("========== lockdown start {} {} {}".format(i, itot, r0))
            elif i >= ld_check and ld:
                ld_check = ld_days_duration + i
                if (delta_cnt <= -ld_days_of_trend_needed and stat < ld_case_threshold) or ld_forced_ending:
                    ld = 0
                    delta_cnt = 0
                    ld_val = 0
                    ld_check = ld_days_of_denial + i
                    ld_endx.append(i+1)
                    ld_endy.append(itot)
                    outp("========== lockdown lifted {0} {1}".format(itot, r0))

        # can we end this?
        if itot > 330000000:
            break

        end_cnt = end_cnt + 1 if itot <= 50 else 0
        if end_cnt == 14:
            tot_days = i + 1 - 14
        if end_cnt >= 14 and i > ev_day + 7:
            break

    dr = dr_visit * cost_dr_visit
    er = er_visit * cost_er_visit
    hr = hosp_admit * cost_admit_per_day * days_admit_duration
    dead = death_visit * cost_death
    tot = dr + er + hr + dead

    if not tot_days:
        duration = 'Continuous'
    else:
        duration = str(tot_days) + ' Days'

    pbuf_end = "Duration: {0},    Health Care Costs: {1:6.3e},    Deaths: {2:6.3e}".format(duration, tot, death_visit)

    outpf(pbuf1)
    outpf(pbuf2)
    outpf(pbuf3)
    outpf(pbuf_end)
    fout.close()

    #  #########################################################

    plt.close('all')

    fig, axes = plt.subplots(ncols=2, nrows=1, constrained_layout=False, gridspec_kw = {'wspace':0, 'hspace':0, 'width_ratios': [5, 1]})
    ax = axes[0]

    ax.plot(plot_x, plot_itot, label='Currently Infected', color='b')
    ax.plot(plot_x, plot_dead, label='Cumulative Dead', color='k')

    date_today = '{}, Day: {}'.format(date.today().strftime("%m/%d/%Y"), ev_day)
    ax.plot([ev_day, ev_day], [0, max(plot_itot)], ls='--', label=date_today, color='g')
    ax.plot([ev_day], [0], marker=6, linestyle='None', color='g', ms=10)

    if plots['plot_new_cases']['val']:
        ax.plot(plot_x, plot_inew, label='New Infections', color='r')

    if ld_allowed:
        if ld_startx and ld_endx:
            ax.plot(ld_startx, ld_starty, marker=5, label='Lockdown Start', linestyle='None', color='r', ms=10)
            ax.plot(ld_endx, ld_endy, marker=4, label='Lockdown End',  linestyle='None', color='r', ms=10)

    if plots['plot_hospital_beds']['val']:
        ax.plot(plot_x, plot_hosp, label='Hospital Beds', color='y')

    if plots['plot_cumulative_cases']['val']:
        ax.plot(plot_x, plot_icum, label='Cumulative Infections', color='m')

    if ll_enabled:
        t = 'Lessons Learned, Day: {}'.format(ll_days_to_deploy)
        x = [ll_days_to_deploy]
        y = [ll_val]
        ax.plot(x, y, label=t, marker='D', color='g', ms=8)

    if test_allowed:
        if not ll_enabled or test_days_to_deploy < ll_days_to_deploy:
            x = [test_days_to_deploy]
            y = [plot_itot[test_days_to_deploy]]
            ax.plot(x, y, label='Testing Deployed', marker='s', color='g', ms=8)

    ax.set_xlabel("Days Since Start")
    ax.set_ylabel("People")
    ax.tick_params(direction='in')

    ax.set_title(pbuf_end)
    ax.legend()

    ax = axes[1]
    ax.set_axis_off()
    ax.set_xlim(left=0, right=1)
    ax.set_ylim(bottom=0, top=1)

    ax.text(.1, 1, pbuf1+pbuf2+pbuf3,
            horizontalalignment='left',
            verticalalignment='top',
            rotation='horizontal',
            size=7)

    plt.subplots_adjust(wspace=0)
    ax.tick_params(labelsize=0, direction='in', top=False, bottom=False, left=False, right=False, labelleft=False, labelbottom=False)
    wm = plt.get_current_fig_manager()
    wm.window.state('zoomed')
    plt.show(block=False)


def menu_maker(defs):

    def _get_vis(child, gchild=None):

        try:
            # are we the top menu of our chain (head)?
            if gchild:

                # make sure we are properly linked and find the element
                # controlling the child menu
                if 'meta' in defs[child] and 'children' in defs[child]['meta'] and gchild in defs[child]['meta']['children']:
                    parm = defs[child]['meta']['children'][gchild]
                else:
                    raise ValueError

                # if the visibility is off, all our sub-menus are off
                if not defs[child][parm]['val']:
                    return False

            # check next layer up?
            if 'meta' in defs[child] and 'parent' in defs[child]['meta']:
                parent = defs[child]['meta']['parent']
                return _get_vis(parent, child)

            # no dependencies
            return True

        except ValueError:
            outp('parent: {}, child: {}, bad linking'.format(child, gchild))
            exit(1)

    children = {}
    sub = {}
    tags = []

    sg.theme('Reddit')  # Add a touch of color

    for title, parms in defs.items():

        disp_title = title

        if 'meta' in parms:
            meta = parms['meta']
            if 'title' in meta:
                disp_title = meta['title']

            if 'children' in meta:
                for menu, elem in meta['children'].items():
                    if menu not in defs:
                        print("Unknown submenu: ", menu)
                        exit(1)
                    elif elem not in parms:
                        print("Unknown element: ", menu + '->' + elem)
                        exit(1)
                    sg_key = title + '-' + elem
                    if sg_key not in children:
                        children.update({sg_key: [menu]})
                    else:
                        children[sg_key].append(menu)

        col1 = [[sg.Text(disp_title, font='Helvetica 10 bold', pad=(0, 0))]]
        col2 = [[sg.Text(" ", font='Helvetica 10 bold', pad=(0, 0))]]

        init_vis = _get_vis(title)

        for name, parm in parms.items():

            if name == 'meta':
                continue

            sg_key = title + '-' + name
            tags.append(sg_key)

            val = parm['val']
            tip = parm['tip']

            if type(val) is bool:
                col1.append([
                    sg.Text(name, pad=(0, 1), tooltip=tip)
                ])
                col2.append([
                    sg.Checkbox("", key=sg_key, default=val, enable_events=True, pad=(0, 0))
                ])
            elif 'drop' in parm:
                col1.append([
                    sg.Text(name, size=(25, 1), pad=(0, 0), tooltip=tip)
                ])
                w = len(max(parm['drop'], key=len)) - 1
                col2.append([
                    sg.InputCombo(parm['drop'], default_value=val, enable_events=True, key=sg_key, size=(w, 1), pad=(0, 1, 0, 0), readonly=True)
                ])
            else:
                col1.append([
                    sg.Text(name, size=(25, 1), pad=(0, 0), tooltip=tip)
                ])
                w = len(val) + 2 if type(val) is str else 5
                col2.append([
                    sg.InputText(key=sg_key, default_text=str(val), size=(w, 1), pad=(0, 0))
                ])

        col = [sg.Column([[sg.Column(col1), sg.Column(col2)]], key=title, visible=init_vis, pad=(0, 0))]
        sub.update({title: col})

    buttons = [sg.Column([[sg.Button('Defaults', key='b-defs'), sg.Button('Plot Infection', key='b-plot')]], pad=(25, 25, 0, 0))]
    col1 = [sg.Column([sub['Outside Lockdown'], sub['Lockdown Parameters'], buttons], pad=(0, 0))]
    col2 = [sg.Column([sub['Testing Parameters'], sub['Lessons Learned'], sub['Lockdown Lessons Learned'], sub['Testing Lessons Learned']], pad=(0, 0))]
    col3 = [sg.Column([sub['Health Care'], sub['Virus Parameters']], pad=(0, 0))]

    layout = [
        [sg.Menu([['&Help', '&About']])],
        col1 + col2 + col3
    ]

    window = sg.Window('COVID-19 Infection Model', layout, resizable=True, grab_anywhere=True, location=(0, 0))

    def _walk_vis(sub, vis):
        window[sub].Update(visible=vis)
        if 'meta' in defs[sub] and 'children' in defs[sub]['meta']:
            for next_sub in defs[sub]['meta']['children']:
                if not vis:
                    _walk_vis(next_sub, False)
                else:
                    _walk_vis(next_sub, _get_vis(next_sub))

    def _set_vis(event, vis):
        if event in children:
            for sub in children[event]:
                _walk_vis(sub, vis)

    def _update_all():
        # set default values
        for tag in tags:
            refs = tag.split('-')
            window[tag].Update(defs[refs[0]][refs[1]]['val'])

        # set default visibility
        for title in sub:
            window[title].Update(visible=_get_vis(title))

    window.read(timeout=0)
    defs = set_model(defs['Outside Lockdown']['response_model']['val'])
    _update_all()

    popup = False
    while True:
        err = False

        event, values = window.read()
        # if event and event in values:
            # print(event, values[event])

        if event == 'Outside Lockdown-response_model':
            defs = set_model(values[event])
            _update_all()

        elif event == 'About':
            sg.popup(About)
            popup = True

        elif event is None:
            if popup:
                continue
            plt.close('all')
            window.close()
            exit(0)

        elif event == 'b-defs':
            defs = get_defaults()
            defs = set_model(defs['Outside Lockdown']['response_model']['val'])
            _update_all()

        elif event == 'b-plot':
            for sg_key in tags:
                keys = sg_key.split('-')
                ref = defs[keys[0]][keys[1]]['val']
                if type(ref) is bool:
                    if ref != values[sg_key]:
                        defs[keys[0]][keys[1]]['val'] = values[sg_key]
                elif type(ref) is float:
                    try:
                        val = float(values[sg_key])
                        if ref != val:
                            if sg_key.find('percent') != -1:
                                if val < 0 or val > 1:
                                    sg.popup_error('{} must be between 0 and 1'.format(keys[1]))
                                    err = True
                                    break
                            defs[keys[0]][keys[1]]['val'] = float(values[sg_key])
                    except ValueError:
                        sg.popup_ok('{} must be numeric'.format(keys[1]))
                        err = True
                        break

                elif type(ref) is int:
                    try:
                        val = int(values[sg_key])
                        if ref != val:
                            defs[keys[0]][keys[1]]['val'] = int(values[sg_key])
                    except ValueError:
                        sg.popup_ok('{} must be integer'.format(keys[1]))
                        err = True
                        break

                elif type(ref) is str:
                    if ref != values[sg_key]:
                        defs[keys[0]][keys[1]]['val'] = values[sg_key]
            if not err:
                run_sim(defs)
                continue

        elif event in children:
            val = values[event]
            pair = event.split('-')
            defs[pair[0]][pair[1]]['val'] = val
            window[event].Update(val)
            _set_vis(event, val)


while True:
    menu_maker(get_defaults())
