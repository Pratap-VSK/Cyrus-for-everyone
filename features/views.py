import json
import math
import sympy as sp
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

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

@require_POST
@csrf_exempt
def calculate_physics(request):

    # LAYER 3: Strict JSON Type validation
    if request.content_type != 'application/json':
        return JsonResponse({'status': 'error', 'message': 'Invalid Data Format!'}, status=415)

    try:
        data = json.loads(request.body)
        formula = data.get('formula')
        
        val1 = float(data.get('val1', 0))
        val2 = float(data.get('val2', 0))
        val3 = float(data.get('val3', 0))
        val4 = float(data.get('val4', 0))
        
        # LAYER 4: DoS & Overflow Protection (Bohat bade numbers block karega)
        max_limit = 10000000  # Max 1 Crore limit
        if abs(val1) > max_limit or abs(val2) > max_limit or abs(val3) > max_limit:
            return JsonResponse({'status': 'error', 'message': 'Values exceed safe server limits!'}, status=400)

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

        # ==================================================================
        # NEWTON'S CLASSICAL MECHANICS & KINEMATICS
        # ==================================================================
        #1. First Equation  of motion (v=u+at)
        elif formula == 'motionFirst':
            u = get_val('val1')
            a = get_val('val2')
            t = get_val('val3')
            result = u + (a*t)
            result_str = f"{result: .4g}"

        #2. second equastion of motion (s = ut + 0.5at^2)

        elif formula == 'motionSecond':
            u = get_val('val1')
            t = get_val('val2')
            a = get_val('val3')
            result = (u * t) + (0.5 * a * (t **2))
            result_str = f"(result: .4g)"

        #3. Third Equation of motion(v^2 = a^2 + 2as)
        
        elif formula == 'motionThird':
            u = get_val('val1')
            a = get_val('val2')
            s = get_val('val3')
            result = (u ** 2) + (2 * a * s)
            if val < 0:
                return = math.sqrt(val)
            result_str = f"(result: .4g)"

        #4. Force (F = ma)
        
        elif formula == 'motionSecond':
            m = get_val('val1')
            a = get_val('val2')
            result = m * a
            result_str = f"(result: .4g)"

        #5. Momentum rate (F = dp/dt)

        elif formula == 'momentumRate':
            dp = get_val('val1')
            dt = get_val('val2')
            if dt == 0:
                return JsonResponse({'status': 'error', 'massage': 'Time derivative (dt) cannot be zero.'})
            result = dp / dt
            result_str = f"{result: .4g}"

        #6. Gravitation Force (F = G * m1 * m2 / r^2)
        elif formula == 'newtonGravity':
            m1 = get_val('val1')
            m2 = get_val('val2')
            r = get_val('val3')
            if r = 0:
                 return JsonResponse({'status': 'error','massage': 'Distance(r) cannot be zero.'})
            G = 6.67430e-11
            result = G * (m1 * m2) / (r ** 2)
            result_str = f"{result: .4e}"

        #7.Newton's Law of Cooling (Rate = -k(T - T_env))

        elif formula == 'newtonCooling':
            k = get_val('val1')
            T = get_val('val2')
            T_env = get_val('val3')
            result = -k * (T - T_env)
            result_str = f"{result: .4g}"

        #8. Newton's Law of Viscosity (tau = mu * (du/dy))
        elif formula == 'newtonViscosity':
            mu = get_val('val1')
            du = get_val('val2')
            dy = get_val('val3')
            if dy == 0:
                return JsonResponse({'status': 'error','massage': 'Layer Distance(dy) cannot be zero.'})
            result = mu * (du / dy)
            result_str = f"{result: .4g}"
        
        #9 Newton's Lens Equation ( f = sqrt(x1 * x2))
        elif formula == 'newtonLens':
            x1 = get_val('val1')
            x2 = get_val('val2')
            if x1 * x2 < 0:
                return JsonResponse({'status': 'error', 'massage': 'Product of Distance cannot be negitive.'})
            result = math.sqrt(x1 * x2)
            result_str = f"{result: .4g}"

        #10. Coefficient of Restitution (e = (v2 -v1) / (u1 -u2))
        elif formula == 'newtonRestitution':
            v1 = get_val('val1')
            v2 = get_val('val2')
            u1 = get_val('val3')
            u2 = get_val('val4')
            if (u1 - u2) == 0:
                return JsonResponse({'status': 'error','massage': 'Initial relative velocity cannot be zero.'})
            result = (v2 - v1) / (u1 -u2)
            result_str =f"{result: .4g}"

        #11. Weight on earth ( W = mg)
        elif formula == 'newtonWeight':
            m = get_val('val1')
            g = 9.81 # Standard  gravity on Earth
            result = m * g
            result_str = f"{result: .4g}"

        #12. Work Done (W = F * s * cos(theta))
        elif formula == 'newtonWork':
            F = get_val('val1')
            s = get_val('val2')
            theta = get_val('val3') # Angle in degrees 
            # Math module user randians, so converting degrees to radians
            radians = math.radians(theta)
            result = F * s * math.cos(radians)
            result_str = f"{result: .4g}"

        #13. Velocity of sound (v = sqrt(P / rho))
        elif formula == 'newtonSound':
            p = get_val('val1')
            rho = get_val('val2')
            if rho <= 0:
                return JsonResponse({'status': 'error','massage': 'Density (rho) must be Srtictly possitive.'})
            result = math.sqrt(p / rho)
            result_str = f"{result: .4g}"

# ==============================================================
#         -:LAPLACE MATHEMATICS: LAPLACE TRANSFORM :-
# ==============================================================
        elif formula == 'laplaceTransform':
            # val1 expects a string mathematical equation in terms of 't' (e.g., "t**2", "sin(t)")
            expr_str = data.get('val1', '')
                
            if not expr_str:
                return JsonResponse({'status': 'error', 'message': 'Mathematical expression cannot be empty.'})
                
            try:
                # Define the time domain (t) and frequency domain (s) symbols
                t, s = sp.symbols('t s')
                    
                # Convert the string input into a SymPy readable symbolic expression
                f_t = sp.sympify(expr_str)
                    
                # Compute the Laplace Transform
                # noconds=True ensures it returns only the F(s) formula, not convergence conditions
                laplace_result = sp.laplace_transform(f_t, t, s, noconds=True)
                    
                # Format the final expression as a string to send back to the frontend
                result_str = str(laplace_result)
                    
            except Exception as e:    
                return JsonResponse({'status': 'error', 'message': f'Invalid mathematical expression format. Ensure you use standard Python syntax (e.g., 2*t instead of 2t). Error details: {str(e)}'})
        

# ======================================================================
#      -:LAPLACE TRANSFORM: ADVACED THEOREMS:-
# ======================================================================
        # 2. iNVERSE Laplace Transform (s -> t)
        elif formula == 'inverseLaplace':
            # val1 expects a string mathematical equation in term of 's' (e.g., "1/(s**2 + 1)")
            expr_str = data.get('val1', '')

            if not expr_str:
                return JsonResponse({'status': 'error', 'massage': 'Expression for F(s) cannot be empty.'})
            try:
                t, s = sp.symbols('t s')
                F_s = sp.sympyfy(expr_str)

                # Compute the Inverse Laplace Transform
                result = sp.inverse_laplace_transform(F_s, s, t)
                result_str = str(result)

            except exception as e:
                return JsonResponse({'status': 'error','massage': ' f"Invalid mathmatical format. Error details: {str(e)} .'})

            # =================================
            #     first shiting theorem
            # =================================

        # 3. First shifting theorem (L{e^(at) * f(t)})
        elif formula == 'laplaceShifting':
            expr_str = data.get('val1', '')
            a_val = get_val('val2')
            if not expr_str:
                return JsonResponse({'status': 'error','massage': ' Expression for f(t) cannot be empty .'})
            try:
                t, s = sp.symbols('t s')
                f_t = sp.sympyfy(expr_str)
                
                # Multiply by  exponential component internally
                shifted_f_t = f_t * sp.exp(a_val * t)

                result = sp.laplace_transform(shifted_f_t, t, s, noconds=true)
                result_str = str(result)
            except exception as e:
                return JsonResponse({'status': 'error','massage': {str(e)} })

            # =====================================
            #      -:LAPLACE DERIVATIVE:-
            # =====================================
        # 4. Laplace Transform of a First  Derivative (L{f'(t)} )
        elif formula == 'laplaceDerivative':

            expr_str = data.get('val1', '')
            f_0 = get_val('val2')
            if not expr_str:
                return JsonResponse({'status': 'error','massage': 'Expression for f(t) cannot be empty.'})
            try:
                t, s = sp.symbols('t s')
                f_t = sp.sympyfy(expr_str)

                #Compute Laplace of the original functionF(s)
                F_s = sp.laplace_transform(F_t, t, s, noconds=true)

                #Apply the derivative theorem-> s*F(s)
                raw_result = (s * F_s) - f_0

                #simplify the mathematical equation for a clear output
                result = sp.simplify(raw_result)
                result_str = str(result)
            except Exception as e:
                return JsonResponse({'status': 'error','massage': {str(e)}})

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Corrupted JSON Payload!'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': 'Internal Server Error.'}, status=500)

def student_page(request):
    return render(request, 'content/student.html')
       