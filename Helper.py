from Const import db
import json, jdatetime, traceback, pytz
from unidecode import unidecode
from datetime import datetime, timedelta

async def process_url_command(mess):
    idk = mess.text.split()

    if len(idk) != 2:
        return 'False: length is not 2'

    try:
        target_id = int(idk[1])
        user_chat_id = str(mess.chat.id)

        if not db.exists("referral", {"userID": target_id}):
            return 'False: target is not in url ids'

        ref = await db.select("referral", ['referrals'], {'userID': target_id})
        current_ref = ref[0]["referrals"] if ref else []

        if user_chat_id not in current_ref:

            current_ref.append(user_chat_id)
            await db.update("referral", {"referrals": current_ref}, where={"userID": target_id})

            wallet = await db.select("wallet", ['coins'], {'userID': target_id})
            current_coins = wallet[0]["coins"] if wallet else 0

            coins_to_award = current_coins * 0.1 + 2500
            await db.update("wallet", {"coins": coins_to_award}, where={"userID": target_id})

        return True

    except ValueError:
        return 'False: value error'
    except Exception as e:
        # Consider logging 'e' for debugging purposes
        return f'False: {e}'
        
day_map = {
    "Saturday": "شنبه",
    "Sunday": "یکشنبه",
    "Monday": "دوشنبه",
    "Tuesday": "سه شنبه",
    "Wednesday": "چهارشنبه",
    "Thursday": "پنجشنبه",
    "Friday": "جمعه"
}

def sorting(the_list, oL):
    oMap = {element: index for index, element in enumerate(oL)}
    def getSortKey(item):
        return oMap.get(item, len(oL))
    result = sorted(the_list, key=getSortKey)
    return result

def get_time(input_day, input_time='23:55'):
    now = datetime.now()
    current_day = now.strftime("%A")  # روز هفته فعلی
    current_time = now.strftime("%H:%M")  # ساعت فعلی

    i = list(map(int, input_time.split(':')))
    
    try:
        input_hour, input_minute = i
        days_of_week = ["شنبه", "یکشنبه", "دوشنبه", "سه شنبه", "چهارشنبه", 'پنجشنبه', "جمعه"]
        input_day_index = days_of_week.index(input_day)

        fa = day_map[current_day]
        current_day_index = days_of_week.index(fa)

        current_hour, current_minute = map(int, current_time.split(':'))
        current_total_minutes = current_hour * 60 + current_minute
        input_total_minutes = input_hour * 60 + input_minute

        if (current_day_index == input_day_index and current_total_minutes < input_total_minutes) or (current_day_index < input_day_index) or (current_day_index == input_day_index and current_total_minutes < input_total_minutes):

            days_to_add = (input_day_index - current_day_index) % 7
        else:

            days_to_add = (input_day_index - current_day_index + 7) % 7  # هفته بعد

        future_date = now + timedelta(days=days_to_add)

        persian_date = jdatetime.datetime.fromgregorian(date=future_date)

        day = persian_date.day
        month = persian_date.month

        months_names = [
            "فروردین", "اردیبهشت", "خرداد",
            "تیر", "مرداد", "شهریور",
            "مهر", "آبان", "آذر",
            "دی", "بهمن", "اسفند"
        ]

        return f"{day} {months_names[month - 1]}"
    except Exception as e:
        print(i, (e), input_day)
        traceback.print_exc()
        return 'error'
   
             
def persian_to_int(number_str):
    latin_number_str = unidecode(number_str)
    return int(latin_number_str)


def load(json_str, fallback=[], verbose=False):
    if json_str is None:
        if verbose:
            print("[!] Warning: Tried to decode None as JSON.")
        return fallback

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        if verbose:
            print(f"[!] JSON Decode Error: {e}")
        try:
            fixed = json_str.replace("'", '"')
            return json.loads(fixed)
        except Exception as e2:
            if verbose:
                print(f"[!] Second attempt failed: {e2}")
            return fallback