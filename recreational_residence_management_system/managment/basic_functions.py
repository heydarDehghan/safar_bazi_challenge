def calculate_total_booking_price(standard_capacity_detail,
                                  extra_capacity_detail,
                                  extra_adult_num,
                                  extra_child_num,
                                  extra_baby_num,
                                  end_date,
                                  start_date
                                  ):
    interval = end_date - start_date
    extra_price = extra_capacity_detail.extra_adult_price * extra_adult_num + extra_capacity_detail. \
        extra_child_price * extra_child_num + extra_capacity_detail.extra_baby_price * extra_baby_num

    extra_price *= interval.days
    standard_price = interval.days * standard_capacity_detail.total_price

    return extra_price + standard_price, standard_price

