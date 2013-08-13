import re
import logging
import datetime

ping_regex = re.compile('(v )*(v)*(\d+\.?\d*)')
long_description_regex = re.compile('(Spring|Summer|Fall)\s(\d){4}(-(\d){4})?')
short_description_regex = re.compile('(\d){4}\s(Sprng|Fall|Summr)')
academic_year_regex = re.compile('(\d){4}-(\d){2}')
term_code_regex = re.compile('(\d){4}')


def negate(func):
    def neg_func(*args):
        if func(args):
            return False
        return True
    return neg_func

def validate_ssh(response):
    return response.succeeded

def validate_lines(*args):
    def validator(value):
        for line in value:
            logging.info(
                "Recieved value '%s' expecting values '%s'" %
                (line, ",".join(str(i) for i in args)))
            broke = False
            for arg in args:
                if not line.count(arg):
                    broke = True
                    break
            if not broke:
                result = True
                logging.info(
                    "Line validation %s" %
                    ("passed" if result else "failed"))
                return result
        result = False
        logging.info("Line validation %s" % ("passed" if result else "failed"))
        return result
    return validator


def validate_regex(regex):
    def validator(value):
        logging.info(
            "Recieved value '%s' expecting pattern '%s'" %
            (value, regex.pattern))
        result = re.match(regex, value)
        logging.info(
            "Regex validation %s" %
            ("passed" if result else "failed"))
        return result
    return validator


def validate_instance(instance):
    def validator(value):
        logging.info(
            "Recieved value '%s' expecting instance '%s'" %
            (value, instance))
        result = isinstance(value, instance)
        logging.info(
            "Instance validation %s" %
            ("passed" if result else "failed"))
        return result
    return validator


def validate_dict(dict_name):
    def validator(value):
        for k, v in value.iteritems():
            if not dict_name[k](v):
                return False
        return True
    return validator

term_dict = {
    "endDate": validate_instance(datetime.datetime),
    "beginDate": validate_instance(datetime.datetime),
    "longDescription": validate_regex(long_description_regex),
    "shortDescription": validate_regex(short_description_regex),
    "academicYear": validate_regex(academic_year_regex),
    "termCode": validate_regex(term_code_regex)
}
