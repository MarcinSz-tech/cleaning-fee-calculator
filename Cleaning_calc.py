import streamlit as st

def calculate_cleaning_price(bedrooms, cleaner_option, custom_cleaning=None, custom_linen=None):
    linen_costs = {1: 9.19, 2: 13.00, 3: 19.13, 4: 25.58, 5: 0}  # 5:0 is a placeholder
    cleaning_charges = {
        1: {1: 30, 2: 28, 3: 34, 4: 48, 5: 0},
        2: {1: 35, 2: 33, 3: 39, 4: 48, 5: 0},
        3: {1: 40, 2: 38, 3: 44, 4: 54, 5: 0},
    }

    if not (1 <= bedrooms <= 5):
        raise ValueError("Invalid number of bedrooms. Please enter a number between 1 and 5.")

    needs_custom_costs = (cleaner_option == 4) or (bedrooms == 5)

    if needs_custom_costs:
        if custom_cleaning is None or custom_linen is None:
            raise ValueError("Custom cleaning and linen costs must be provided for this selection.")
        cleaning = custom_cleaning
        linen = custom_linen
    else:
        if cleaner_option not in [1, 2, 3] or bedrooms not in cleaning_charges[cleaner_option]:
            raise ValueError("No specific cleaning charge found for this cleaner and bedroom count.")
        cleaning = cleaning_charges[cleaner_option][bedrooms]
        linen = linen_costs[bedrooms]

    base_price = linen + cleaning
    final_price = (base_price * 100) / 65  # Maintain 35% margin
    return round(final_price, 2)


# Streamlit UI
st.title("Cleaning Fee Calculator")

bedrooms = st.selectbox("Number of bedrooms:", [1, 2, 3, 4, 5])

if bedrooms == 5:
    st.markdown("**Custom cleaning and linen costs required for 5-bedroom properties.**")
    cleaner_option = 4
else:
    cleaner_option = st.selectbox("Who is cleaning?", [1, 2, 3, 4], format_func=lambda x: ["Natalie", "AGS", "Lucid", "Other"][x-1])

needs_custom = (bedrooms == 5) or (cleaner_option == 4)

custom_cleaning = custom_linen = None
if needs_custom:
    custom_cleaning = st.number_input("Custom cleaning cost (£):", min_value=0.0, format="%.2f")
    custom_linen = st.number_input("Custom linen cost (£):", min_value=0.0, format="%.2f")

if st.button("Calculate"):
    try:
        price = calculate_cleaning_price(bedrooms, cleaner_option, custom_cleaning, custom_linen)
        owner_contributions = {1: 10, 2: 14, 3: 17, 4: 20, 5: 25}
        owner_cost = owner_contributions.get(bedrooms, 0)
        guest_cost = round(price - owner_cost, 2)

        st.success(f"Total price (incl. cleaners cost, linen, markup): £{price}")
        st.info(f"Guest is charged: £{guest_cost}\n\nOwner covers linen cost (net): £{owner_cost}")

    except ValueError as e:
        st.error(f"Error: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
