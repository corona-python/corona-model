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
Corona Virus Instructional Project
Author: Robert Leyendecker (c) 2020
Version: .2, May 3, 2020
Python: 3.8, Menus: PySimpleGUI, Plots: matplotlib, Windows Exe: Pyinstaller
Build: pyinstaller -w -F --hidden-import="pkg_resources.py2_warn" corona.py

This program is intended to explore the political choices available to confront a pandemic.
Each choice involves a policy decision that has life or death consequences. 
- Do we spend tax money on testing or do we give tax breaks to the rich in an election year?
- Do we focus on early containment/mitigation or gamble with the hope that it will just go away?
- How many deaths will occur as a result of our decision?

* Hover over menu items to see a brief description of parameters *

Influential Parameters:
- Percent sick traced outside lockdown
- Days of denial
- Early end of lockdown
- How quickly we react to lockdown changes (attack/decay)
- Days before test results
- Lessons learned
- Health care quality (percent sick who die)

Number of infections is estimated as 2X number of govt. reported cases.
This is due to large number of asymptomatic cases and inconsistent reporting.
Lockdown attack/decay is implemented as simple first order recursive section.
Test tracing is weighted inversely by days to results.

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
    if fout:
        fout.write("{0}\n".format(s))


def outf(s):
    if fout:
        fout.write("{0}\n".format(s))


def get_defaults():
    defs = {
        'Outside Lockdown': {
            'response_model': {'val': 'Political (USA)', 'tip': 'Baseline response model.',
                               'drop': {
                                   'Political (USA)': None,
                                   'Medical (Slower)': None,
                                   'Medical (Faster)': None,
                                   'Medical (Taiwan)': None,
                                   'No Response': None}},
            'response_speed': {'val': 'slow', 'tip': 'How quickly we deploy our response.',
                               'drop': {'slow': .995, 'medium': .99, 'fast': .987}},
            'percent_sick_traced': {'val': .10, 'tip': 'Percentage of contacts from suspected cases, traced and isolated.'},
            'pst_attack': {'val': 'medium', 'hide': True, 'attack': {'slow': .93, 'medium': .915, 'fast': .85}},
            'allow_testing': {'val': True, 'tip': 'Allow routine tests of people with symptoms?'},
            'allow_learning': {'val': False, 'tip': 'Have we learned anything that we can apply in the future?'},
            'allow_lockdown': {'val': True, 'tip': 'Allow lockdown as a strategy?'},
            'end_sim': {'val': 'auto', 'tip': 'When do end simulation?',
                        'drop': {'auto': 0, '180 days': 180, '360 days': 360, '540 days': 540, '720 days': 720}},
            'show_virus': {'val': False, 'tip': 'Show virus parameters.'},
            'show_health_care': {'val': False, 'tip': 'Show health care parameters.'},
            'plot_cumulative_cases': {'val': False, 'tip': 'Are we flattening the infection curve?'},
            'plot_new_cases': {'val': False, 'tip': 'Plot the new cases being discovered'},
            'create_corona_csv': {'val': False, 'tip': 'Output corona.csv file in current directory'},
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
            'days_of_trend_needed': {'val': 30, 'tip': 'Days of trending data are needed before changing lockdown state.'},
            'days_min_duration': {'val': 30, 'tip': 'Minimum  number of days for a lockdown.'},
            'case_threshold': {'val': 1000, 'tip': 'Maximum number of cases to end lockdown.'},
            'forced_ending': {'val': True, 'tip': 'Do we end lockdown regardless of of the trend or number of cases?'},
            'meta': {
                'parent': 'Outside Lockdown'
            }
        },
        'Testing Parameters': {
            'days_to_deploy': {'val': 0, 'tip': 'Days before routine testing begins?'},
            'test_attack': {'val': 'slow', 'hide': True, 'attack': {'slow': .93, 'medium': .915, 'fast': .9}},
            'days_before_result': {'val': 5, 'tip': 'Days before test results.'},
            'percent_random_tested': {'val': 0.0, 'tip': 'Number of random people tested'},
            'percent_sick_tested': {'val': .1, 'tip': 'Percentage of people tested who show milder symptoms.'},
            'percent_accuracy': {'val': .8, 'tip': 'Percentage of accurate positive test results.'},
            'percent_pos_traced': {'val': .25, 'tip': 'Percentage of contacts from positive test case, traced and isolated.'},
            'meta': {
                'parent': 'Outside Lockdown'
            }
        },
        'Lessons Learned': {
            'response_speed': {'val': 'slow', 'tip': 'How fast do we deploy lessons learned?',
                               'drop': {'slow': .9975, 'medium': .995, 'fast': .9875}},
            'days_to_deploy': {'val': 0, 'tip': 'Days before we start deploying any lessons learned.'},
            'percent_sick_traced': {'val': .1, 'tip': 'Percentage of contacts from suspected cases, traced and isolated.'},
            'pst_attack': {'val': 'medium', 'hide': True, 'attack': {'slow': .93, 'medium': .915, 'fast': .9}},
            'allow_lockdown': {'val': False, 'tip': 'Can we lockdown as part of lessons learned?'},
            'allow_testing': {'val': True, 'tip': 'Can we test as part of lessons learned?'},
            'meta': {
                'children': {
                    'Testing Lessons Learned': 'allow_testing',
                    'Lockdown Lessons Learned': 'allow_lockdown'
                },
                'parent': 'Outside Lockdown'
            }
        },
        'Lockdown Lessons Learned': {
            'days_of_denial': {'val': 0, 'tip': 'Minimum number of days we wait before invoking lockdown.'},
            'percent_isolated': {'val': .75, 'tip': 'Percentage of people observing isolation during lockdown.'},
            'days_of_trend_needed': {'val': 14, 'tip': 'Days of infection trend data needed to change state of lockdown.'},
            'forced_ending': {'val': False, 'tip': 'End lockdown regardless of case load or trend.'},
            'meta': {
                'parent': 'Lessons Learned'
            }
        },
        'Testing Lessons Learned': {
            'test_attack': {'val': 'slow', 'hide': True, 'attack': {'slow': .93, 'medium': .915, 'fast': .9}},
            'days_before_result': {'val': 5, 'tip': 'Days before test result known.'},
            'percent_random_tested': {'val': 0.0, 'tip': 'Percentage of people tested regardless of symptoms.'},
            'percent_sick_tested': {'val': .1, 'tip': 'Percentage of symptomatic people tested.'},
            'percent_accuracy': {'val': .8, 'tip': 'Percentage of accurate positive test results.'},
            'percent_pos_traced': {'val': .25, 'tip': 'Percentage of contacts from positive test case, traced and isolated?'},
            'meta': {
                'parent': 'Lessons Learned'
            }
        },
        'Virus Parameters': {
            'date_start': {'val': '1/31/2020', 'tip': 'Not recommended to change.'},
            'days_before_symptoms': {'val': 5, 'tip': 'Not recommended to change.'},
            'days_before_free': {'val': 21, 'tip': 'Not recommended to change.'},
            'percent_with_symptoms': {'val': .5, 'tip': 'Percentage of people showing symptoms.'},
            'percent_with_mild_symptoms': {'val': .8, 'tip': 'Percentage of people showing mild symptoms.'},
            'r0': {'val': 1.3825, 'tip': 'Not recommended to change.'},
            'r0_random': {'val': False, 'tip': 'Not recommended to change.'},
            'r0_jitter': {'val': .001, 'tip': 'Not recommended to change.'},
            'meta': {
                'parent': 'Outside Lockdown'
            }
        },
        'Health Care': {
            'percent_dr_visit': {'val': .2, 'tip': 'Percentage of symptomatic people who visit doctor''s office.'},
            'percent_er_visit': {'val': .05, 'tip': 'Percentage of symptomatic people who visit the ER.'},
            'percent_symptom_admit': {'val': .2, 'tip': 'Percentage of symptomatic people admitted to hospital.'},
            'days_before_admit': {'val': 10, 'tip': 'Days before symptomatic people enter hospital.'},
            'days_admit_duration': {'val': 6, 'tip': 'Days spent admitted in hospital.'},
            'percent_symptom_death': {'val': .02, 'tip': 'Percentage of symptomatic people who die.'},
            'cost_admit_per_day': {'val': 8000, 'tip': 'Daily cost of hospital stay.'},
            'cost_dr_visit': {'val': 400, 'tip': 'Cost of DR office visit.'},
            'cost_er_visit': {'val': 5000, 'tip': 'Cost of ER visit'},
            'cost_death': {'val': 10000, 'tip': 'Cost of death.'},
            'meta': {
                'parent': 'Outside Lockdown'
            }
        }
    }

    defs['Testing Parameters']['days_to_deploy']['val'] = defs['Lockdown Parameters']['days_of_denial']['val'] + defs['Lockdown Parameters']['days_min_duration']['val']
    defs['Lessons Learned']['days_to_deploy']['val'] = defs['Lockdown Parameters']['days_of_denial']['val'] + defs['Lockdown Parameters']['days_min_duration']['val']
    defs['Health Care']['percent_dr_visit']['val'] = 1 - defs['Virus Parameters']['percent_with_mild_symptoms']['val']

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

    if model == 'Medical (Slower)':
        default['response_speed']['val'] = 'slow'
        default['allow_testing']['val'] = True
        default['allow_learning']['val'] = False
        ld['days_of_denial']['val'] = 45
        ld['forced_ending']['val'] = True
        test['days_to_deploy']['val'] = 60
        test['percent_sick_tested']['val'] = .1

    elif model == 'Medical (Faster)':
        default['response_speed']['val'] = 'fast'
        default['allow_testing']['val'] = True
        default['allow_learning']['val'] = False
        ld['days_of_denial']['val'] = 45
        ld['forced_ending']['val'] = True
        test['days_to_deploy']['val'] = 45
        test['percent_sick_tested']['val'] = .1
        test['percent_random_tested']['val'] = .01

    elif model == 'Medical (Taiwan)':
        default['response_speed']['val'] = 'fast'
        default['percent_sick_traced']['val'] = .2
        default['allow_learning']['val'] = False
        default['allow_testing']['val'] = True
        default['allow_lockdown']['val'] = True
        ld['days_of_denial']['val'] = 14
        ld['percent_isolated']['val'] = .8
        ld['days_of_trend_needed']['val'] = 7
        ld['case_threshold']['val'] = 50
        ld['forced_ending']['val'] = False
        ll['response_speed']['val'] = 'fast'
        test['days_to_deploy']['val'] = 21
        test['days_before_result']['val'] = 2
        test['percent_pos_traced']['val'] = .3
        test['percent_sick_tested']['val'] = .25
        health['percent_symptom_death']['val'] = .02

    elif model == 'No Response':
        default['response_speed']['val'] = 'slow'
        default['allow_testing']['val'] = False
        default['allow_learning']['val'] = False
        default['allow_lockdown']['val'] = False

    return defs


def get_keys(dct, value):
    return [key for key in dct if (dct[key] == value)]


def get_drop(sub, name):
    mapped = sub[name]['drop'][sub[name]['val']]
    return mapped if mapped != '' else name


def run_sim(parms):
    global fout

    default = parms['Outside Lockdown']
    ld = parms['Lockdown Parameters']
    test = parms['Testing Parameters']
    care = parms['Health Care']
    virus = parms['Virus Parameters']
    ll = parms['Lessons Learned']
    ll_test = parms['Testing Lessons Learned']
    ll_ld = parms['Lockdown Lessons Learned']
    plots = default

    # output data to csv?
    if default['create_corona_csv']['val']:
        fout = open("corona.csv", "w+")

    # percent of we find to isolate after contact with person showing symptoms
    response_model = default['response_model']['val']

    # percent of we find to isolate after contact with person showing symptoms
    response_speed = get_drop(default, 'response_speed')

    # percent of we find to isolate after contact with person showing symptoms
    percent_sick_traced = default['percent_sick_traced']['val']

    # alpha to lift lockdown
    pst_attack = default['pst_attack']['attack'][default['response_speed']['val']]

    # how do we end sim
    end_sim = get_drop(default, 'end_sim')

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

    test_attack = test['test_attack']['attack'][default['response_speed']['val']]

    # days to deploy testing
    test_days_to_deploy = test['days_to_deploy']['val']

    # days before test results
    test_days_before_result = test['days_before_result']['val']

    # percent of carriers random tested
    test_percent_random_tested = test['percent_random_tested']['val']

    # percent of carriers tested before symptoms
    test_percent_sick_tested = test['percent_sick_tested']['val']

    # percent who correctly test positive
    test_percent_accuracy = test['percent_accuracy']['val']

    # percent of we find to isolate after contact with person who has pos test
    test_percent_pos_traced = test['percent_pos_traced']['val']

    # after first lockdown, improved tracing and detection
    ll_response_speed = get_drop(ll, 'response_speed')
    ll_percent_sick_traced = ll['percent_sick_traced']['val']
    ll_pst_attack = ll['pst_attack']['attack'][ll['response_speed']['val']]
    ll_days_to_deploy = ll['days_to_deploy']['val']
    ll_ld_allowed = ll['allow_lockdown']['val']
    ll_ld_days_of_denial = ll_ld['days_of_denial']['val']
    ll_ld_days_of_trend_needed = ll_ld['days_of_trend_needed']['val']
    ll_ld_percent_isolated = ll_ld['percent_isolated']['val']
    ll_ld_forced_ending = ll_ld['forced_ending']['val']
    ll_test_allowed = ll['allow_testing']['val']
    ll_test_attack = ll_test['test_attack']['attack'][ll['response_speed']['val']]
    ll_test_percent_pos_traced = ll_test['percent_pos_traced']['val']
    ll_test_days_before_result = ll_test['days_before_result']['val']
    ll_test_percent_accuracy = ll_test['percent_accuracy']['val']
    ll_test_percent_random_tested = ll_test['percent_random_tested']['val']
    ll_test_percent_sick_tested = ll_test['percent_sick_tested']['val']

    pbuf1 = ""
    pbuf1 += "Baseline Response: {}\n".format(response_model)
    pbuf1 += "Response Speed: {0}, w: {1:.3f}\n".format(default['response_speed']['val'], response_speed)
    pbuf1 += "  Percent Sick Traced: {0:0.3f}, w: {1:0.3f}\n".format(percent_sick_traced, pst_attack)
    pbuf1 += "  End Sim: {}".format(end_sim)
    if not ld_allowed:
        pbuf1 += "  No Lockdown\n"
    else:
        pbuf1 += "  Denial Before Lockdown: {0}\n".format(ld_days_of_denial)
        pbuf1 += "  Lockdown Duration: {0}\n".format(ld_days_duration)
        pbuf1 += "  Days Trend Before Change: {0}\n".format(ld_days_of_trend_needed)
        pbuf1 += "  Isolated: {0:0.3f}\n".format(ld_percent_isolated)
        pbuf1 += "  Forced Ending: {0}\n".format(ld_forced_ending)
        pbuf1 += "  Begin/End Case Threshold: {0}\n".format(ld_case_threshold)
    if not test_allowed:
        pbuf1 += "  No Initial Testing\n"
    else:
        pbuf1 += "  Days to Deploy Testing: {}\n".format(test_days_to_deploy)
        pbuf1 += "  Attack: {0:.3f}\n".format(test_attack)
        pbuf1 += "  Test Accuracy: {}, Wait: {}\n".format(test_percent_accuracy, test_days_before_result)
        pbuf1 += "  Tested, Random {},  Sick {}\n".format(test_percent_random_tested, test_percent_sick_tested)
        pbuf1 += "  Isolated: {0:0.4f}\n".format(test_percent_pos_traced)

    if ll_allowed:
        pbuf1 += "\nDays to Lessons Learned: {0}\n".format(ll_days_to_deploy)
        pbuf1 += "  Response Speed: {0}, w: {1:0.3f}\n".format(ll['response_speed']['val'], ll_response_speed)
        pbuf1 += "  Sick Traced: {0:0.3f}, w: {1:0.3f}\n".format(ll_percent_sick_traced, ll_pst_attack)
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
            pbuf1 += "  Attack: {0:.3f}\n".format(ll_test_attack)
            pbuf1 += "  Test Accuracy: {}, Wait: {}\n".format(ll_test_percent_accuracy, ll_test_days_before_result)
            pbuf1 += "  Tested, Random {},  Sick {}\n".format(ll_test_percent_random_tested, ll_test_percent_sick_tested)
            pbuf1 += "  Isolated: {0:0.4f}\n".format(ll_test_percent_pos_traced)
    else:
        pbuf1 += "  No Lessons Learned\n"

    # ###############  things we cannot control  ###############

    # days before detection (symptoms, test result)
    days_before_symptoms = virus['days_before_symptoms']['val']

    # days until no longer contagious
    days_before_free = virus['days_before_free']['val']

    # percent who show any symptoms
    percent_with_symptoms = virus['percent_with_symptoms']['val']

    # of those with symptoms, percent who show mild symptoms
    percent_with_mild_symptoms = virus['percent_with_mild_symptoms']['val']

    # infection rate without symptoms
    r0 = virus['r0']['val']
    r0_random = virus['r0_random']['val']
    r0_jitter = virus['r0_jitter']['val']
    date_start = virus['date_start']['val']

    pbuf2 = ""
    pbuf2 += "\nVirus Parameters\n"
    pbuf2 += "  Start Date (m/d/y): {}\n".format(date_start)
    pbuf2 += "  Infections Per Day: {0}\n".format(r0)
    pbuf2 += "  Percent With Symptoms: {0}\n".format(percent_with_symptoms)
    pbuf2 += "  Percent With Mild Symptoms: {0}\n".format(percent_with_mild_symptoms)
    pbuf2 += "  Days Before Free: {0}\n".format(days_before_free)
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
    pbuf3 += "  Visit Dr Office: {0:.2f}, ${1} per visit\n".format(percent_dr_visit, cost_dr_visit)
    pbuf3 += "  Visit ER: {0}, ${1} per visit\n".format(percent_er_visit, cost_er_visit)
    pbuf3 += "  Hospital: {0}, ${1} per day\n".format(percent_symptom_admit, cost_admit_per_day)
    pbuf3 += "  Dead: {0}, ${1} per death\n".format(percent_symptom_dead, cost_death)

    #############################################################

    public_list = list()
    admit_list = list()
    sick_list = list()
    inf_act_list = list()
    iso_list = list()
    ld_endx = list()
    ld_endy = list()
    ld_startx = list()
    ld_starty = list()

    # scale tracing by how long needed to wait for result
    test_trace = test_percent_pos_traced / test_days_before_result if test_days_before_result else test_percent_pos_traced
    ll_test_trace = ll_test_percent_pos_traced / ll_test_days_before_result if ll_test_days_before_result else ll_test_percent_pos_traced

    # percent who have more severe symptoms, no test needed
    # to suspect case, will self-isolate, will contact trace
    percent_with_severe_symptoms = (1 - percent_with_mild_symptoms) * percent_with_symptoms

    # milder symptoms, may get tested to confirm
    percent_with_mild_symptoms *= percent_with_symptoms

    admit_cum = 0
    admit_act = 0
    sick_act = 0
    sick_cum = 0
    dr_visit_cum = 0
    er_visit_cum = 0
    death_visit_cum = 0

    inf_act = 1
    ld = False
    ld_val = 0
    delta_cnt = 0
    ld_check = ld_days_of_denial
    last_stat = 0
    hosp_admit = 0
    iso = 0
    iso_act = 0

    ld_state = 0
    test_mild_state = 0
    test_mild_trace = 0
    test_rand_state = 0
    test_rand_trace = 0
    sev_sick_state = 0
    sev_sick_trace = 0

    public = 1
    ll_enabled = 0
    ll_val = 0
    end_cnt = 0
    tot_days = 0
    test_enabled = False
    inf_cum = 0
    ev_day = event_day(date_start)

    plot_inf_act = list()
    plot_x = list()
    plot_dead = list()
    plot_iso = list()
    plot_inf_cum = list()
    plot_inew = list()

    test_time = test_days_to_deploy + days_before_symptoms + test_days_before_result

    if not (test_percent_sick_tested and test_percent_accuracy and test_percent_pos_traced):
        test_allowed = False

    if not (ll_test_percent_sick_tested and ll_test_percent_accuracy and ll_test_percent_pos_traced):
        ll_test_allowed = False

    outf("end of day, infected, isolated, hospitalized, lockdown active")

    for i in range(0, 730):

        outf(
            "end of: {0:4d}, inf: {1:10.2f}, hosp: {2:10.2f}, ld_delta: {3:d}, r0: {4:1.3f}, iso: {5:10.2f}, public: {6:10.2f}, ld_cnt: {7:d}, trace: {8:0.4f} / {9:0.4f}".format(
                i + 1, inf_act, admit_act, delta_cnt, r0, iso_act, public, ld, test_trace, ld_state))

        outf("{0:4d}, {1:10.2f}, {2:10.2f}, {3:10.2f}, {4:10.2f}".format(i + 1, inf_act, iso_act, admit_act, ld_val))

        # accumulate isolated per day
        iso_act += iso
        iso_list.append(iso)

        # current number of active infections
        inf_new = public + iso
        inf_act += inf_new
        inf_act_list.append(inf_new)

        # cumulative infections
        inf_cum += public + iso

        # save number of new infections, not isolated
        public_list.append(public)

        # our plot lists
        plot_x.append(i)
        plot_inf_act.append(inf_act)
        plot_inf_cum.append(inf_cum)
        plot_iso.append(iso_act)
        plot_dead.append(death_visit_cum)
        plot_inew.append(inf_new)

        # start of new day
        iso = 0
        if r0_random:
            r0 = random.uniform(r0 - r0_jitter, r0 + r0_jitter)
        public *= r0

        if not test_enabled and test_allowed and i >= test_time:
            test_enabled = True

        if not ll_enabled and ll_allowed and i >= ll_days_to_deploy:
            outp("========== deploy lessons learned {} {}==========".format(i, ld, inf_act))

            percent_sick_traced = ll_percent_sick_traced
            pst_attack = ll_pst_attack

            if ll_ld_allowed:
                ld_check = i + ll_ld_days_of_denial
                ld_days_of_denial = ll_ld_days_of_denial
                ld_days_of_trend_needed = ll_ld_days_of_trend_needed
                ld_percent_isolated = ll_ld_percent_isolated
                ld_forced_ending = ll_ld_forced_ending
                ld_allowed = True
            else:
                ld_allowed = False

            if ll_test_allowed:
                test_trace = ll_test_trace
                test_attack = ll_test_attack
                test_percent_random_tested = ll_test_percent_random_tested
                test_percent_sick_tested = ll_test_percent_sick_tested
                test_percent_accuracy = ll_test_percent_accuracy
                test_time = ll_days_to_deploy + days_before_symptoms + ll_test_days_before_result
                test_enabled = True
            else:
                test_enabled = False

            ll_val = inf_act
            ll_enabled = 1

        # find out how many we isolate during lockdown
        if ld:
            x = ld_percent_isolated
        else:
            x = 0

        ld_state = response_speed * ld_state + (1 - response_speed) * x
        x = public * ld_state
        iso += x
        public -= x

        # self-isolation and tracing
        if i >= days_before_symptoms:
            # People who self-isolate due to more severe symptoms
            # that clearly indicate infection. we assume
            # some contacts will be traced and found and isolated.
            # even though they may go to dr, the symptoms clearly
            # indicate suspected case, test may be pos later, but
            # isolation begins now, no test needed. Note severe
            # doesn't nec mean bad enough for hospital,
            x = percent_with_severe_symptoms
            sev_sick_state = pst_attack * sev_sick_state + (1 - pst_attack) * x

            x = percent_sick_traced
            sev_sick_trace = pst_attack * sev_sick_trace + (1 - pst_attack) * x

            pos = public * (sev_sick_state + sev_sick_trace)
            iso += pos
            public -= pos

        # random test and trace
        if test_enabled and test_percent_random_tested:
            # ramp up testing
            x = test_percent_random_tested * test_percent_accuracy
            test_rand_state = test_attack * test_rand_state + (1 - test_attack) * x

            # ramp up tracing
            x = test_trace
            test_rand_trace = test_attack * test_rand_trace + (1 - test_attack) * x

            # number who test positive and need to be isolated
            pos = public * (test_rand_state + test_rand_trace)
            iso += pos
            public -= pos

        # symptomatic test and trace (mild)
        if test_enabled and i >= test_time:
            # number of people showing positive results and isolated
            x = percent_with_mild_symptoms * test_percent_sick_tested * test_percent_accuracy
            test_mild_state = test_attack * test_mild_state + (1 - test_attack) * x

            # ramp up tracing
            x = test_trace
            test_mild_trace = test_attack * test_mild_trace + (1 - test_attack) * x

            # number who test positive and need to be isolated
            pos = public * (test_mild_state + test_mild_trace)
            iso += pos
            public -= pos

        # update our health stats
        sick_list.append(public * percent_with_symptoms)
        sick_act += public * percent_with_symptoms
        sick_cum += sick_act

        # here try to count hospital beds and deaths
        # and add up total costs
        if i >= days_before_admit:

            # cumulative er visits
            er_visit_cum = sick_cum * percent_er_visit

            # cumulative dr visits
            dr_visit_cum = sick_cum * percent_dr_visit

            # cumulative number who will die
            death_visit_cum = dr_visit_cum * percent_symptom_dead

            # add in those on iso list
            admit_act = sick_act * percent_symptom_admit

            # add to hospital list
            admit_list.append(admit_act)

            # accumulate hospital admits
            admit_cum += admit_act

            if i >= days_admit_duration:
                admit_act -= admit_list.pop(0) if admit_list else 0

        if i >= days_before_free:
            inf_act -= inf_act_list.pop(0)
            iso_act -= iso_list.pop(0)
            sick_act -= sick_list.pop(0)

        stat = inf_act
        # print("{}, allow {}, check {}, ld {}, frc {}, thresh {}, stat {}/{}, ll {}, cnt {}, trend {}, den {}".format(
        # i, ld_allowed, ld_check, ld, ld_forced_ending, ld_case_threshold, stat, last_stat, ll_enabled,
        # delta_cnt, ld_days_of_trend_needed, ld_days_of_denial))

        if ld_allowed:
            if not ld and stat > last_stat:
                delta_cnt += 1
            elif ld and stat < last_stat:
                delta_cnt += 1
            else:
                delta_cnt = 0
            last_stat = stat

            # replace with moving average?
            if i >= ld_check:
                ld_check += ld_days_of_denial
                if not ld and delta_cnt >= ld_days_of_trend_needed and stat >= ld_case_threshold:
                    delta_cnt = 0
                    ld_check = i + ld_days_duration
                    ld = True
                    ld_val = stat
                    ld_startx.append(i)
                    ld_starty.append(inf_act)
                    # print("========== {} lockdown start {} {}".format(i, inf_act, r0))
                elif ld and ((delta_cnt >= ld_days_of_trend_needed and stat < ld_case_threshold) or ld_forced_ending):
                    delta_cnt = 0
                    ld = False
                    ld_val = 0
                    ld_endx.append(i)
                    ld_endy.append(inf_act)
                    # print("========== {} lockdown lifted {} {}".format(i, inf_act, r0))

        # can we end this?
        if inf_act > 330000000:
            break
        elif end_sim:
            if i >= end_sim:
                break
        elif not ld and i > 90 and inf_act <= ld_case_threshold:
            end_cnt = end_cnt + 1
            if end_cnt == 14:
                tot_days = i + 1 - 14
                break
        else:
            end_cnt = 0

    dr_tot = dr_visit_cum * cost_dr_visit
    er_tot = er_visit_cum * cost_er_visit
    hr_tot = hosp_admit * cost_admit_per_day * days_admit_duration
    dead_tot = death_visit_cum * cost_death
    cost_tot = dr_tot + er_tot + hr_tot + dead_tot

    if not tot_days:
        duration = 'Continuous'
    else:
        duration = str(tot_days) + ' Days'

    pbuf_end = "Duration: {}    Medical: ${}    Deaths: {}".format(
        duration, format(int(cost_tot), ',d'), format(int(death_visit_cum), ',d'))

    outpf(pbuf1)
    outpf(pbuf2)
    outpf(pbuf3)
    outpf(pbuf_end)
    if fout:
        fout.close()

    #  #########################################################

    plt.close('all')

    fig, axes = plt.subplots(ncols=2, nrows=1, constrained_layout=False, gridspec_kw={'wspace': 0, 'hspace': 0, 'width_ratios': [5, 1]})
    ax = axes[0]

    ax.plot(plot_x, plot_inf_act, label='Currently Infected', color='b')
    ax.plot(plot_x, plot_dead, label='Cumulative Dead', color='k')

    date_today = '{}, Day: {}'.format(date.today().strftime("%m/%d/%Y"), ev_day)
    ax.plot([ev_day, ev_day], [0, max(plot_inf_act)], ls='--', label=date_today, color='g')
    ax.plot([ev_day], [0], marker=6, linestyle='None', color='g', ms=10)

    if plots['plot_new_cases']['val']:
        ax.plot(plot_x, plot_inew, label='New Infections', color='r')

    if ld_startx:
        ax.plot(ld_startx, ld_starty, marker=5, label='Lockdown Start', linestyle='None', color='r', ms=10)
    if ld_endx:
        ax.plot(ld_endx, ld_endy, marker=4, label='Lockdown End', linestyle='None', color='r', ms=10)

    if plots['plot_cumulative_cases']['val']:
        ax.plot(plot_x, plot_inf_cum, label='Cumulative Infections', color='m')

    if ll_enabled:
        t = 'Lessons Learned, Day: {}'.format(ll_days_to_deploy)
        x = [ll_days_to_deploy]
        y = [ll_val]
        ax.plot(x, y, label=t, marker='D', color='g', ms=8)

    if test_allowed:
        if not ll_enabled or test_days_to_deploy < ll_days_to_deploy:
            t = 'Testing Start, Day: {}'.format(test_days_to_deploy)
            x = [test_days_to_deploy]
            y = [plot_inf_act[test_days_to_deploy]]
            ax.plot(x, y, label=t, marker='s', color='g', ms=8)

    ax.set_xlabel("Days Since Start")
    ax.set_ylabel("People")
    ax.tick_params(direction='in')

    ax.set_title(pbuf_end)
    ax.legend()

    ax = axes[1]
    ax.set_axis_off()
    ax.set_xlim(left=0, right=1)
    ax.set_ylim(bottom=0, top=1)

    ax.text(.1, 1, pbuf1 + pbuf2 + pbuf3,
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

            if 'hide' in parm and parm['hide']:
                continue

            elif name == 'meta':
                continue

            sg_key = title + '-' + name
            tags.append(sg_key)

            val = parm['val']
            tip = parm['tip']

            if 'radio' in parm:
                buts = []
                for but in parm['radio']:
                    v = True if val == but else False
                    buts.append(sg.Radio(but, name, enable_events=False, key=sg_key + '-' + but, pad=(0, 1, 0, 0), default=v))
                col1.append([
                    sg.Text(name, size=(25, 1), pad=(0, 0), tooltip=tip)
                ])
                col2.append(buts)
            elif 'drop' in parm:
                col1.append([
                    sg.Text(name, size=(25, 1), pad=(0, 0), tooltip=tip)
                ])
                opts = [opt for opt in parm['drop']]
                w = len(max(opts, key=len))
                col2.append([
                    sg.InputCombo(opts, default_value=val, enable_events=True, key=sg_key, size=(w, 1), pad=(0, 1, 0, 0), readonly=True)
                ])
            elif type(val) is bool:
                col1.append([
                    sg.Text(name, pad=(0, 1), tooltip=tip)
                ])
                col2.append([
                    sg.Checkbox("", key=sg_key, default=val, enable_events=True, pad=(0, 0))
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
        #     print(event, values[event])

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
                        # print(keys, ref, values[sg_key], defs[keys[0]][keys[1]]['val'])
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
