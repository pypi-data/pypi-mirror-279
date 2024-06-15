from datetime import datetime
import pytz
from Countrydetails import country
from typing import List, Dict, Any, Optional

class CancellationPolicy:
    def __init__(self, check_in_date: str):
        self.current_datetime = datetime.now()
        self.free_cancellation_policy = None
        self.check_in_date = check_in_date
        self.partner_cp = []
        self.cn_polices = []
        

    def format_date(self, date_str: Optional[str] = None) -> str:
        if date_str is None:
            return self.current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        parsed_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
        return parsed_date.strftime("%Y-%m-%d %H:%M:%S")

    def get_check_in_date(self) -> str:
        return self.check_in_date
    
    def dida_date_format(self, date_str: str) -> str:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d %H:%M:%S")
    
    def hp_format_date(self, date_str: str) -> datetime:
        try:
            return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            pass
        
        try:
            return datetime.strptime(date_str, "%m/%d/%Y")
        except ValueError:
            pass
        
        try:
            return datetime.strptime(date_str, "%d/%m/%Y")
        except ValueError:
            raise ValueError(f"Date format for '{date_str}' is not recognized.")
        
    def tbo_format_date(self, date_str: str) -> datetime:
        return datetime.strptime(date_str, "%d-%m-%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
    
    def parse_cancellation_policies(self, free_cancellation: bool, total_partner: float, parsed_policies: List[Dict[str, Any]]) -> Dict[str, Any]:
        cancellation_policies_text = []
        if free_cancellation:
            cancellation_type = "Free cancellation"
        else:
            cancellation_type = "Non-Refundable"
        
        partial_booking = False
        cp_dates_added = []
        cp_i = 0
        end_policy = False
        first_free_sts = False
        
        if parsed_policies and len(parsed_policies) > 0:
            for key, policy in enumerate(parsed_policies):
                ref_amt = 100 - ((total_partner - float(policy['amount'])) / total_partner) * 100
                ref_amt = round(ref_amt)
                
                if ref_amt == 0:
                    if first_free_sts:
                        cancellation_policies_text.pop()
                    ref_amt = 100
                    free_cancellation = True
                    first_free_sts = True
                    cancellation_type = "Free cancellation"
                elif ref_amt == 100:
                    ref_amt = 0
                    end_policy = True
                
                if ref_amt > 0:
                    partial_booking = True

                replace_start = str(policy['start'])
                time_start = datetime.strptime(replace_start, '%Y-%m-%d %H:%M:%S').strftime('%I:%M %p')
                date_start = datetime.strptime(replace_start, '%Y-%m-%d %H:%M:%S').strftime('%d %b %Y')

                replace_end = str(policy['end'])
                time_end = datetime.strptime(replace_end, '%Y-%m-%d %H:%M:%S').strftime('%I:%M %p')
                date_end = datetime.strptime(replace_end, '%Y-%m-%d %H:%M:%S').strftime('%d %b %Y')

                start_date_str = date_start + ' ' + time_start
                end_date_str = date_end + ' ' + time_end

                if free_cancellation and cp_i == 0:
                    cancellation_policies_text.append(f"Receive a {ref_amt}% refund for your booking if you cancel before {date_end} at {time_end}")
                elif cp_i == 0:
                    cancellation_policies_text.append(f"Receive a {ref_amt}% refund for your booking if you cancel before {date_end} at {time_end}")
                else:
                    if ref_amt != 0:
                        cancellation_policies_text.append(f"Receive a {ref_amt}% refund for your booking if you cancel between {start_date_str} and {end_date_str}")
                cp_i += 1

            if end_policy:
                cancellation_policies_text.append(f"If you cancel your reservation after {start_date_str}, you will not receive a refund. The booking will be non-refundable.")
            else:
                cancellation_policies_text.append(f"If you cancel your reservation after {end_date_str}, you will not receive a refund. The booking will be non-refundable.")

            if not partial_booking and not free_cancellation:
                cancellation_type = "Non-Refundable"
                cancellation_policies_text = ["You won't be refunded if you cancel this booking"]
            elif not free_cancellation and partial_booking:
                cancellation_type = "Partial refund"
        else:
            cancellation_type = "Non-Refundable"
            cancellation_policies_text = ["You won't be refunded if you cancel this booking"]

        self.cn_polices = {
            'type': cancellation_type,
            'text': cancellation_policies_text
        }
        return self.cn_polices

    # parse ratehawk cancellation policy
    def parse_ratehawk_cancellation_policy(self,pricing: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        cp = []
        if 'cancellation_penalties' in pricing[0] and 'policies' in pricing[0]['cancellation_penalties']:
            check_in_date = self.get_check_in_date()
            
            for policy in pricing[0]['cancellation_penalties']['policies']:
                start_at = policy.get('start_at', datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
                end_at = policy.get('end_at', check_in_date)
                self.partner_cp.append({
                    'start': self.format_date(start_at),
                    'end': self.format_date(end_at),
                    'amount': policy['amount_show'],
                    'currency': pricing[0]['currency_code'] if 'currency_code' in pricing[0] else "USD"
                })
                free_cancellation_before = pricing[0]["cancellation_penalties"]["free_cancellation_before"]           
                if free_cancellation_before is None or free_cancellation_before == "":
                    free_cancellation_before = None
                if policy['amount_show'] == '0.00' and free_cancellation_before is not None and self.free_cancellation_policy is None:
                    self.free_cancellation_policy = True
        return self.partner_cp
    # Rakuten provide in UTC timezone
    def parse_rakuten_cancellation_policy(self,room_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        cancellation_policies = []
        policy_rules = room_data['cancellation_policy']
        currency_code = room_data['room_info']['room_rate_currency']
        policies = policy_rules['cancellation_policies']

        for rule_data in policies:
            if 'date_from' in rule_data and rule_data['date_from']:
                start_date = self.format_date(rule_data['date_from'])
                start_date_obj = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
                if start_date_obj < self.current_datetime:
                    start_date = self.current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            else:
                start_date = self.current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                start_date_obj = self.current_datetime

            if 'date_to' in rule_data and rule_data['date_to']:
                end_date = self.format_date(rule_data['date_to'])
                end_date_obj = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
            else:
                end_date = self.current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                end_date_obj = self.current_datetime
            # case 1 as per rakuten cancellation_policy will regularly return a date that is already in the past (i.e. 1999-01-01T17:47:00Z) This indicates that the penalty_percentage applies from the time of booking
            if start_date_obj < self.current_datetime and end_date_obj < self.current_datetime:
                continue 
            if  start_date_obj > self.current_datetime and end_date_obj <= self.current_datetime:
                end_date = self.format_date(self.get_check_in_date())
            room_price = 10 #room_data['room_info']['room_rate']
            if rule_data['penalty_percentage'] == 0:
                percentage = 0
            elif rule_data['penalty_percentage'] == 100:
                percentage = 100
            else:
                percentage = 100 - rule_data['penalty_percentage']
            amount_percentage = room_price / 100
            percentage_amount = amount_percentage * percentage
            cp = {
                'start': start_date,
                'end': end_date,
                'amount': percentage_amount,
                'currency': currency_code
            }
            cancellation_policies.append(cp)
            if  rule_data['penalty_percentage'] == 0 and self.free_cancellation_policy is None:
                self.free_cancellation_policy = True

        return cancellation_policies
    
    # please be kindly note all the cancelation are based on Beijing time
    def parse_dida_cancellation_policy(self,pricing: Dict[str, Any], total_price: float) -> List[Dict[str, Any]]:
        cp = []
        check_in_date = self.format_date(self.get_check_in_date())
        
        if 'RatePlanCancellationPolicyList' in pricing and len(pricing['RatePlanCancellationPolicyList']) > 0:
            temp_array = []
            i = 0
            last_date = None
            
            for k, policy in enumerate(pricing['RatePlanCancellationPolicyList']):
                if i == 0:
                    start_at = self.current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    start_at = last_date
                end_at = policy.get('FromDate', check_in_date)
                end_at = self.dida_date_format(end_at)
                end_date_obj = datetime.strptime(end_at, "%Y-%m-%d %H:%M:%S")
                if end_date_obj < self.current_datetime:
                    continue
                    #end_at = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                last_date = end_at
                i += 1
                if policy['Amount'] == 0:
                    amount_rtn = 0
                elif policy['Amount'] == total_price:
                    amount_rtn = total_price
                else:
                    amount_rtn = total_price - policy['Amount']
                self.partner_cp.append({
                    'start': start_at,  # date format (2021-07-11 00:00:00)
                    'end': end_at,
                    'amount': amount_rtn,
                    'currency': pricing['Currency']
                })
                if  policy['Amount'] == 0 and self.free_cancellation_policy is None:
                    self.free_cancellation_policy = True
        
        return self.partner_cp
    
    # Hp provide in UTC timezone
    def parse_hp_cancellation_policy(self, pricing: Dict[str, Any], total_hp: float) -> List[Dict[str, Any]]:
        global free_cancellation_policy
        cancellation_policies = []
        temp_array = []
        s_end_date = None
        if 'freeCancellationCutOff' in pricing and pricing['freeCancellationCutOff']:
            s_start_at = self.current_datetime
            s_end_date = self.hp_format_date(pricing['freeCancellationCutOff'])
            s_start_at = s_start_at.strftime("%Y-%m-%d %H:%M:%S")
            s_end_date = s_end_date.strftime("%Y-%m-%d %H:%M:%S")
            if s_end_date > s_start_at:
                first_cp = {
                    'start': s_start_at,
                    'end': s_end_date,
                    'amount': 0,
                    'currency': pricing['currencyCode']
                }
                cancellation_policies.append(first_cp)
        last_date = None
        pricing['cancelPenalties'] = sorted(pricing['cancelPenalties'], key=lambda x: datetime.strptime(x['deadline'], "%m/%d/%Y"))
        for i, policy in enumerate(pricing['cancelPenalties']):
            if policy not in temp_array and 'deadline' in policy and policy['deadline']:
                temp_array.append(policy)
                if i == 0 and s_end_date is not None:
                    start_at = s_end_date
                elif i == 0:
                    start_at = self.current_datetime
                else:
                    start_at = last_date
                end_at_str = policy['deadline'].replace(',', '')
                
                end_at = self.hp_format_date(end_at_str)
                if end_at == start_at:
                    continue
                if end_at <  self.current_datetime:
                    continue
                last_date = end_at
                i += 1
            
                amount = policy.get('price', policy.get('amount', 0))
                if isinstance(start_at, str):
                    s_check_date = datetime.strptime(start_at, "%Y-%m-%d %H:%M:%S")
                else:
                    s_check_date = datetime.strptime(start_at.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
                if isinstance(end_at, str):
                    e_check_date = datetime.strptime(end_at, "%Y-%m-%d %H:%M:%S")
                else:
                    e_check_date = datetime.strptime(end_at.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
                if e_check_date < s_check_date:
                    continue
                if amount == 0:
                    ret_amount = 0
                else:
                    ret_amount = total_hp - amount if total_hp > amount else total_hp
                
                cp = {
                    'start': start_at.strftime("%Y-%m-%d %H:%M:%S"),
                    'end': end_at.strftime("%Y-%m-%d %H:%M:%S"),
                    'amount': ret_amount,
                    'currency': pricing.get('currencyCode', 'USD')
                }
                self.partner_cp.append(cp)

                if pricing.get('freeCancellation') and self.free_cancellation_policy is None:
                    self.free_cancellation_policy = True

        return self.partner_cp
    
    # Tbo cancellation policy method
    # please be kindly note all the cancelation are based on Beijing time
    def parse_tbo_cancellation_policy(self,pricing: Dict[str, Any], total_price: float) -> List[Dict[str, Any]]:
        global free_cancellation_policy
        cp = []
        check_in_date = self.format_date(self.get_check_in_date())
        
        if len(pricing) > 0:
            temp_array = []
            i = 0
            last_date = None
            
            for k, policy in enumerate(pricing):
                if i == 0:
                    start_at = self.current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    start_at = last_date
                end_at = policy.get('FromDate', check_in_date)
                end_at = self.tbo_format_date(end_at)
                end_date_obj = datetime.strptime(end_at, "%Y-%m-%d %H:%M:%S")
                if end_date_obj < self.current_datetime:
                    continue
                    #end_at = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                last_date = end_at
                i += 1
                if policy['ChargeType'] == 'Fixed':
                    can_amount     = total_price - policy['CancellationCharge']
                    if can_amount == total_price:
                        can_amount = 0.0
                else:
                    if policy['CancellationCharge'] == 0.0:
                        can_amount = 0.0
                    else:
                        percentage     = policy['CancellationCharge'] / 100
                        prcent_amount  = percentage * total_price
                        can_amount     = total_price - prcent_amount
                        if percentage == 1.0:
                            can_amount = total_price
                self.partner_cp.append({
                    'start': start_at,  # date format (2021-07-11 00:00:00)
                    'end': end_at,
                    'amount': can_amount,
                    'currency': 'USD'
                })
                if  can_amount == 0 and self.free_cancellation_policy is None:
                    self.free_cancellation_policy = True
        
        return self.partner_cp
    # this method will convert property cancellation policy according to the property timezone
    def convert_to_timezone(self, date_str, from_tz_str, to_tz_str):
        from_tz = pytz.timezone(from_tz_str)
        to_tz = pytz.timezone(to_tz_str)

        # Parse the date string
        naive_datetime = datetime.strptime(date_str, '%d %b %Y %I:%M %p')
        # Localize to the from_tz
        localized_datetime = from_tz.localize(naive_datetime)
        # Convert to the target timezone
        converted_datetime = localized_datetime.astimezone(to_tz)

        return converted_datetime
        
    
