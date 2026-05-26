import json
import math
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# ==========================================
# 1. SMART CALCULATOR VIEWS
# ==========================================
def home_page(request):
    return render(request, 'content/home.html')

def calculator_page(request):
    # Renders the calculator UI from the content folder
    return render(request, 'content/calculator.html')

@csrf_exempt
def process_calculation(request):
    # Processes basic mathematical expressions securely
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            expression = data.get('expression', '')
            
            # Basic security check to allow only math characters
            allowed_chars = set("0123456789+-*/(). ")
            if not set(expression).issubset(allowed_chars):
                return JsonResponse({'error': 'Invalid characters in expression'}, status=400)
            
            # Evaluate the mathematical string
            result = eval(expression)
            
            # Format integer outputs clearly
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            elif isinstance(result, float):
                result = round(result, 5)
                
            return JsonResponse({'result': result})
            
        except ZeroDivisionError:
            return JsonResponse({'error': 'Cannot divide by zero'}, status=400)
        except Exception:
            return JsonResponse({'error': 'Invalid mathematical format'}, status=400)
            
    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)


# ==========================================
# 2. HEIGHT CONVERTER VIEWS
# ==========================================
def height_page(request):
    # Renders the height converter UI
    return render(request, 'content/height.html')

@csrf_exempt
def calculate_height(request):
    # Processes height unit conversions based on a standard meter
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            val = float(data.get('value', 0))
            from_unit = data.get('from_unit', 'cm')
            to_unit = data.get('to_unit', 'm')

            # Conversion rates relative to 1 Meter (Base Unit)
            rates = {
                'mm': 1000.0,
                'cm': 100.0,
                'm': 1.0,
                'in': 39.3701,
                'ft': 3.28084,
                'yd': 1.09361,
            }

            if from_unit not in rates or to_unit not in rates:
                return JsonResponse({'error': 'Invalid Units Provided'}, status=400)

            in_meters = val / rates[from_unit]
            final_result = in_meters * rates[to_unit]

            formatted_result = int(final_result) if final_result.is_integer() else round(final_result, 5)
            return JsonResponse({'result': formatted_result})

        except ValueError:
            return JsonResponse({'error': 'Invalid Numerical Input'}, status=400)
        except Exception:
            return JsonResponse({'error': 'Internal Server Error'}, status=500)

    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)


# ==========================================
# 3. DISTANCE CONVERTER VIEWS
# ==========================================
def distance_page(request):
    # Renders the distance converter UI
    return render(request, 'content/distance.html')

@csrf_exempt
def calculate_distance(request):
    # Processes long-distance geographical unit conversions
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            val = float(data.get('value', 0))
            from_unit = data.get('from_unit', 'm')
            to_unit = data.get('to_unit', 'km')

            # Conversion rates relative to 1 Meter
            dist_rates = {
                'm': 1.0, 
                'km': 0.001, 
                'mi': 0.000621371, 
                'yd': 1.09361, 
                'ft': 3.28084, 
                'nmi': 0.000539957
            }

            if from_unit not in dist_rates or to_unit not in dist_rates:
                return JsonResponse({'error': 'Invalid Units Provided'}, status=400)

            in_meters = val / dist_rates[from_unit]
            final_ans = in_meters * dist_rates[to_unit]
            
            formatted_result = int(final_ans) if final_ans.is_integer() else round(final_ans, 5)
            return JsonResponse({'result': formatted_result})
            
        except ValueError:
            return JsonResponse({'error': 'Invalid Numerical Input'}, status=400)
        except Exception:
            return JsonResponse({'error': 'Internal Server Error'}, status=500)

    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)


# ==========================================
# 4. AREA CONVERTER VIEWS
# ==========================================
def area_page(request):
    # Renders the geographical area converter UI
    return render(request, 'content/area.html')

@csrf_exempt
def calculate_area(request):
    # Processes land and area measurement conversions including regional units
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            val = float(data.get('value', 0))
            from_unit = data.get('from_unit', 'sq_m')
            to_unit = data.get('to_unit', 'sq_ft')

            # Conversion rates relative to 1 Square Meter (Base Unit)
            area_rates = {
                'sq_m': 1.0,
                'sq_km': 0.000001,
                'sq_ft': 10.7639,
                'sq_yd': 1.19599,
                'acre': 0.000247105,
                'hectare': 0.0001,
                'bigha': 0.000395368,  # UP Standard
                'biswa': 0.00790737    # UP Standard
            }

            if from_unit not in area_rates or to_unit not in area_rates:
                return JsonResponse({'error': 'Invalid Units Provided'}, status=400)

            in_base_unit = val / area_rates[from_unit]
            final_ans = in_base_unit * area_rates[to_unit]
            
            formatted_result = int(final_ans) if final_ans.is_integer() else round(final_ans, 5)
            return JsonResponse({'result': formatted_result})
            
        except ValueError:
            return JsonResponse({'error': 'Invalid Numerical Input'}, status=400)
        except Exception:
            return JsonResponse({'error': 'Internal Server Error'}, status=500)

    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)


# ==========================================
# 5. WEIGHT CONVERTER VIEWS
# ==========================================
def weight_page(request):
    # Renders the industrial and standard weight scale UI
    return render(request, 'content/weight.html')

@csrf_exempt
def calculate_weight(request):
    # Processes mass conversions mapping micro to macro units
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            val = float(data.get('value', 0))
            from_unit = data.get('from_unit', 'kg')
            to_unit = data.get('to_unit', 'g')

            # Conversion rates relative to 1 Gram (Base Unit)
            weight_rates = {
                'g': 1.0,
                'mcg': 1000000.0,
                'mg': 1000.0,
                'ct': 5.0,
                'kg': 0.001,
                'q': 0.00001,
                'ton': 0.000001,
                'lb': 0.00220462,
                'oz': 0.035274,
                'st': 0.000157473
            }

            if from_unit not in weight_rates or to_unit not in weight_rates:
                return JsonResponse({'error': 'Invalid Units Provided'}, status=400)

            in_base_grams = val / weight_rates[from_unit]
            final_ans = in_base_grams * weight_rates[to_unit]
            
            formatted_result = int(final_ans) if final_ans.is_integer() else round(final_ans, 5)
            return JsonResponse({'result': formatted_result})
            
        except ValueError:
            return JsonResponse({'error': 'Invalid Numerical Input'}, status=400)
        except Exception:
            return JsonResponse({'error': 'Internal Server Error'}, status=500)

    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)


# ==========================================
# 6. GST TAX CALCULATOR VIEWS
# ==========================================
def gst_page(request):
    # Renders the commercial GST billing interface
    return render(request, 'content/finance.html')

@csrf_exempt
def calculate_gst(request):
    # Processes commercial tax ledgers including inclusive and exclusive taxation algorithms
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            amount = float(data.get('amount', 0))
            rate = float(data.get('rate', 18))
            action = data.get('action', 'add')
            supply_type = data.get('supply_type', 'intra')

            if amount < 0 or rate < 0:
                return JsonResponse({'status': 'error', 'error': 'Negative arithmetic values are disallowed'}, status=400)

            # Route calculation based on addition or deduction of tax
            if action == 'add':
                total_gst = amount * (rate / 100)
                grand_total = amount + total_gst
                base_amount = amount
            else:
                grand_total = amount
                base_amount = amount / (1 + (rate / 100))
                total_gst = grand_total - base_amount

            # Allocate jurisdiction tax brackets
            cgst = sgst = igst = 0.0
            if supply_type == 'intra':
                cgst = total_gst / 2
                sgst = total_gst / 2
            else:
                igst = total_gst

            # Build standardized fixed-float accounting response payload
            response_payload = {
                'status': 'success',
                'base_amount': f"{base_amount:.2f}",
                'total_gst': f"{total_gst:.2f}",
                'cgst': f"{cgst:.2f}",
                'sgst': f"{sgst:.2f}",
                'igst': f"{igst:.2f}",
                'grand_total': f"{grand_total:.2f}"
            }
            return JsonResponse(response_payload)

        except (ValueError, TypeError):
            return JsonResponse({'status': 'error', 'error': 'Malformed dataset parameters'}, status=400)
        except Exception:
            return JsonResponse({'status': 'error', 'error': 'Server arithmetic processing failure'}, status=500)

    return JsonResponse({'status': 'error', 'error': 'Only POST method is allowed'}, status=405)

@csrf_exempt
def calculate_physics(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            formula = data.get('formula')
            
            # Fetching up to 4 values, defaulting to 0 if not provided
            val1 = float(data.get('val1', 0))
            val2 = float(data.get('val2', 0))
            val3 = float(data.get('val3', 0))
            val4 = float(data.get('val4', 0)) # Specifically for Angle (theta) in Magnetic Force
            
            result = 0.0
            
            # ==========================================
            # 1. IoT HARDWARE & SENSORS
            # ==========================================
            if formula == 'ledResistor':
                # R = (Vs - Vf) / I
                result = (val1 - val2) / val3 if val3 != 0 else 0
            
            elif formula == 'vdiv':
                # Vout = Vin * (R2 / (R1 + R2))
                result = val1 * (val3 / (val2 + val3)) if (val2 + val3) != 0 else 0
            
            elif formula == 'adcConvert':
                # Voltage = (ADC_Value * System_Voltage) / (Resolution - 1)
                result = (val1 * val2) / (val3 - 1) if (val3 - 1) != 0 else 0
            
            elif formula == 'battery':
                # Hours = Capacity (mAh) / Load (mA)
                result = val1 / val2 if val2 != 0 else 0
                
            elif formula == 'energy':
                # E = Power * Time (Joules)
                result = val1 * val2

            # ==========================================
            # 2. BASIC CIRCUITRY
            # ==========================================
            elif formula == 'voltage':
                # V = I * R
                result = val1 * val2
            
            elif formula == 'current':
                # I = V / R
                result = val1 / val2 if val2 != 0 else 0
            
            elif formula == 'resistance':
                # R = V / I
                result = val1 / val2 if val2 != 0 else 0
            
            elif formula == 'power':
                # P = V * I
                result = val1 * val2

            # ==========================================
            # 3. CAPACITANCE & ELECTROMAGNETISM
            # ==========================================
            elif formula == 'rctime':
                # tau = R * C
                result = val1 * val2
                
            elif formula == 'charge':
                # Q = C * V
                result = val1 * val2
                
            elif formula == 'transformer':
                # Vs = Vp * (Ns / Np)
                result = val1 * (val3 / val2) if val2 != 0 else 0
                
            elif formula == 'magneticForce':
                # F = I * L * B * sin(theta)
                result = val1 * val2 * val3 * math.sin(math.radians(val4))

            # ==========================================
            # 4. THERMODYNAMICS & ENVIRONMENT
            # ==========================================
            elif formula == 'heat':
                # H = I^2 * R * t
                result = (val1 ** 2) * val2 * val3
                
            elif formula == 'tempCF':
                # F = (C * 9/5) + 32
                result = (val1 * 9/5) + 32
                
            elif formula == 'tempKC':
                # K = C + 273.15
                result = val1 + 273.15

            # ==========================================
            # 5. MOTION, FORCES & ENERGY
            # ==========================================
            elif formula == 'velocity':
                # v = u + at
                result = val1 + (val2 * val3)
                
            elif formula == 'distance':
                # s = ut + 1/2*a*t^2
                result = (val1 * val3) + (0.5 * val2 * (val3 ** 2))
                
            elif formula == 'kineticEnergy':
                # K.E = 1/2 * m * v^2
                result = 0.5 * val1 * (val2 ** 2)
                
            elif formula == 'potentialEnergy':
                # P.E = m * g * h
                result = val1 * val2 * val3
                
            elif formula == 'basicPressure':
                # P = F / A
                result = val1 / val2 if val2 != 0 else 0
                
            elif formula == 'pressure':
                # Hydrostatic P = rho * g * h
                result = val1 * val2 * val3

            # ==========================================
            # 6. OPTICS & RF COMMUNICATION
            # ==========================================
            elif formula == 'wavelength':
                # lambda = c / f (where c is speed of light: ~299,792,458 m/s)
                result = 299792458 / val1 if val1 != 0 else 0
                
            elif formula == 'frequency':
                # f = c / lambda
                result = 299792458 / val1 if val1 != 0 else 0
                
            elif formula == 'illuminance':
                # E = I / d^2
                result = val1 / (val2 ** 2) if val2 != 0 else 0
                
            # Rounding result up to 4 decimals for a clean UI render
            formatted_result = round(result, 4)
            return JsonResponse({'status': 'success', 'result': formatted_result})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            
    return JsonResponse({'status': 'error', 'message': 'Invalid Request'}, status=400)


def student_page(request):
    return render(request, 'content/student.html')