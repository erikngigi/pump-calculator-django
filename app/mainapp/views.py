from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.utils import timezone
from .forms import CustomUserCreationForm, TradeCalculator, ContactForm
from .decorators import allowed_users, check_expiration
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import math

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Extracting the cleaned data from the form
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            package = form.cleaned_data['package']
            message = form.cleaned_data['message']

            # Create the email subject and message
            full_message = f"Name: {name}\nEmail: {email}\nPackage: {package}\nMessage: {message}"
            send_mail(
                subject,
                full_message,
                settings.EMAIL_HOST_USER,  # From email
                ['admin@example.com'],  # To email
                fail_silently=False,
            )
            return render(request, 'contact_success.html')  # Redirect to a success page
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

@require_POST
def select_package(request):
    # Get the package selected by the user
    package_name = request.POST.get('package_name')
    
    # Send an email alert to the admin
    if package_name:
        send_mail(
            subject='Package Selected',
            message=f'A user selected the {package_name} package.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
        )
        return JsonResponse({'message': 'Success'})
    else:
        return JsonResponse({'message': 'Failed'}, status=400)

def login_view(request):
    # check if user is already logged in
    if request.user.is_authenticated:
        return redirect('calculator')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('calculator')
        else:
            messages.error(request, "Invalid username or password.", extra_tags='danger')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def pricing(request):
    return render(request, 'pricing.html')

@login_required(login_url="login")
def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out!')
    return redirect('home')

def signup_view(request):
    # check if user is already logged in
    if request.user.is_authenticated:
        return redirect('calculator')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)  # Create user but don't save to the database yet
            user.set_password(form.cleaned_data['password1'])  # Set password securely
            user.save()  # Save the user with all fields
            messages.success(request, 'You have successfully signed up!', extra_tags='success')
            return redirect('login')
        else:
            messages.error(request, 'There was an error with your signup. Please correct the errors below.', extra_tags='danger')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'signup.html', {'form': form})

@login_required
def profile_view(request):
    user = request.user
    signup_date = user.date_joined  # Get the date the user signed up
    countdown_end = signup_date + timezone.timedelta(days=30)  # Calculate the countdown end date
    remaining_time = countdown_end - timezone.now()  # Calculate remaining time

    # Check if the countdown has expired
    countdown_expired = remaining_time.total_seconds() <= 0

    # If the countdown has expired, redirect to the "account_expired" page
    # if countdown_expired:
    #     return redirect('account_expired')  # Change 'account_expired' to your actual URL name

    return render(request, 'profile.html', {
        'user': user,
        'countdown_expired': countdown_expired,
        'remaining_time': remaining_time,
    })

def custom_404(request):
    return render(request, '404.html', status=404)

def home_view(request):
    return render(request, 'home.html')

def account_expired(request):
    return render(request, 'accountexpired.html')

@login_required
@check_expiration
  # Apply the decorator here
# @allowed_users(allowed_roles=['admin', 'editor'], redirect_url='pricing')  # Redirect to 'pricing' if not allowed
@require_http_methods(["GET", "POST"])
# @allowed_users(allowed_roles='customer')
def trade_calculations_view(request):
    if request.method == "GET":
        trade_calc = TradeCalculator()
        return render(request, "calculator.html", {"trade_calc": trade_calc})
    
    trade_calc = TradeCalculator(request.POST)

    if trade_calc.is_valid():
        # Clean and store all necessary variables
        entry_a = trade_calc.cleaned_data["entry_line_a"]
        entry_b = trade_calc.cleaned_data["entry_line_b"]
        entry_price = trade_calc.cleaned_data["entry_price"]
        leverage_entry = trade_calc.cleaned_data["leverage_entry"]
        trade_selection = trade_calc.cleaned_data["trade_options"]
        account_size = trade_calc.cleaned_data["account_size"]

        # Calculate the percentage per grid price for a short and long trade
        if trade_selection == "short":
            ppg_price = (entry_a - entry_price) / entry_price * 100
        elif trade_selection == "long":
            ppg_price = (entry_price - entry_a) / entry_a * 100
        else:
            raise ValueError("invalid trade selection")

        # Calculate the power entry and the turbo entry
        power_entry = round(28/ppg_price, 0)
        turbo_entry = round(2+power_entry, 0)

        # Calculate the position size input by the user
        position_size = math.trunc(account_size * 0.1)
        custom_position_size = math.trunc(position_size / 2)

        # Calculate position limit from the position size
        position_limit_1 = position_size * 0.075
        position_limit_2 = position_size * 0.15
        position_limit_3 = position_size * 0.275
        position_limit_4 = position_size * 0.5

        # Calcuate totals from the position limit sizes
        position_limit_total_1 = position_limit_1 + position_limit_2
        position_limit_total_2 = position_limit_total_1 + position_limit_3
        position_limit_total_3 = position_limit_total_2 + position_limit_4

        # Calculate the line difference for a short and long trade
        if trade_selection == "short":
            line_diff = entry_b - entry_a
        elif trade_selection == "long":
            line_diff = entry_a - entry_b
        else:
            raise ValueError("invalid trade selection")

        line_diff = round(line_diff, 8)

        # Calculate the price levels based on the power entry for a short and long trade
        minimum_level = 2
        if trade_selection == "short":
            power_entry_price = entry_b + ((power_entry - minimum_level) * line_diff) if power_entry >= minimum_level else entry_price
            turbo_entry_price = entry_b + ((turbo_entry - minimum_level) * line_diff) if turbo_entry >= minimum_level else entry_a + line_diff
        elif trade_selection == "long":
            power_entry_price = entry_b - ((power_entry - minimum_level) * line_diff) if power_entry >= minimum_level else entry_price
            turbo_entry_price = entry_b - ((turbo_entry - minimum_level) * line_diff) if turbo_entry >= 2 else entry_a - line_diff
        else:
            raise ValueError("invalid trade selection")

        # Spread calculations
        if trade_selection == "short":
            spread_price = power_entry_price - line_diff
        elif trade_selection == "long":
            spread_price = power_entry_price + line_diff
        else:
            raise ValueError("invalid trade selection")

        # Calculate targets
        targets = {}
        for i in range(1, 6):
            multiplier = i * 2 - 2
            if trade_selection == "short":
                targets[f"target_{i}"] = round(entry_b + (multiplier * line_diff), 8)
            elif trade_selection == "long":
                targets[f"target_{i}"] = round(entry_b - (multiplier * line_diff), 8)

        # Add power and turbo entry prices to the targets dictionary
        targets["power_entry_target"] = round(power_entry_price, 8)
        targets["turbo_entry_target"] = round(turbo_entry_price, 8)

        # Calculate grids
        grids = {}
        for i in range(1, 5):
            if trade_selection == "short":
                grids[f"grid_{i}"] = ((targets[f"target_{i}"] - entry_price) / entry_price) * 100
            elif trade_selection == "long":
                grids[f"grid_{i}"] = ((targets[f"target_{i}"] - entry_price) / entry_price) * 100

        # Calculate spot entries
        spot_entries = {}
        if trade_selection == "short":
            spot_entries["spot_50"] = round(1.5 * entry_price, 8)
            spot_entries["spot_70"] = round(1.7 * entry_price, 8)
            spot_entries["spot_100"] = round(2 * entry_price, 8)
        elif trade_selection == "long":
            spot_entries["spot_50"] = round(0.5 * entry_price, 8)
            spot_entries["spot_70"] = round(0.3 * entry_price, 8)
            spot_entries["spot_100"] = round(0.1 * entry_price, 8)

        # Generate comments
        comments = {}
        comments["comment_1"] = "Entry is Okay" if ppg_price > 5 else "Use 4 Levels Up as Entry or Line 2 Price" if ppg_price < 5 else " "
        comments["comment_2"] = "Grid is Okay" if ppg_price > 12.5 else "Be Careful with the Top Up" if ppg_price < 12.5 else " "
        comments["comment_3"] = "Grid is Okay. Use this Top Up" if grids["grid_1"] > 28 else "Grid is Not Okay. Use the next Top Up" if grids["grid_1"] < 28 else " "
        comments["comment_4"] = "Grid is Okay. Use this Top Up" if grids["grid_1"] > 54 else "Grid is Not Okay. Use the next Top Up" if grids["grid_1"] < 54 else " "
        comments["comment_5"] = "Grid is Okay. Use this Top Up" if grids["grid_1"] > 84 else "Grid is Not Okay. Use the next Top Up" if grids["grid_1"] < 84 else " "

        suggestion_1 = "Enter $" + str(position_size) if ppg_price > 12.5 else "Enter $" + str(custom_position_size) + " here and $" + str(custom_position_size) + " at Line 2" if ppg_price < 5 else " "

        # Dynamic table titles and body details
        title_name = "Short" if trade_selection == "short" else "Long"
        trade_move = "Above" if trade_selection == "short" else "Below"
        price_levels = "Up" if trade_selection == "short" else "Down"

        context = {
            "entry_line_a": round(entry_a, 8),
            "entry_line_b": round(entry_b, 8),
            "ppg_price": round(ppg_price, 2),
            "power_entry": math.trunc(round(power_entry, 0)),
            "turbo_entry": math.trunc(round(turbo_entry, 0)),
            "line_diff": round(line_diff, 8),
            "entry_price": round(entry_price, 8),
            "leverage_entry": math.trunc(round(leverage_entry, 8)),
            "power_entry_price": round(power_entry_price, 8),
            "turbo_entry_price": round(turbo_entry_price, 8),
            "spread_price": round(spread_price, 8),
            "position_limit_1": round(position_limit_1, 2),
            "position_limit_2": round(position_limit_2, 2),
            "position_limit_3": round(position_limit_3, 2),
            "position_limit_4": round(position_limit_4, 2),
            "position_limit_total_1": round(position_limit_total_1, 2),
            "position_limit_total_2": round(position_limit_total_2, 2),
            "position_limit_total_3": round(position_limit_total_3, 2),
            "account_size": account_size,
            "title_name": title_name,
            "trade_move": trade_move,
            "suggestion_1": suggestion_1,
            "price_levels": price_levels,
            **targets,
            **grids,
            **spot_entries,
            **comments
        }

        return render(request, "tables.html", context)

    return render(request, "calculator.html", {"trade_calc": trade_calc})
