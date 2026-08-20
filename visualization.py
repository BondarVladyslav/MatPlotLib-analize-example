from collections import Counter

from database.ORM import (
    select_sites_with_avg_time,
    select_responses_time,
    select_responses_status_code,
)
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from numpy import percentile
from utils import format_long_link, count_availability

fig = plt.figure(figsize=(16, 9), constrained_layout=True)
gs = fig.add_gridspec(2, 2)

ax_speed = fig.add_subplot(gs[0, 0])
ax_uptime = fig.add_subplot(gs[1, 0])
ax_codes = fig.add_subplot(gs[:, 1])


def configure_avg_time_graph(ax_speed):
    column_height = 0.4

    default_avg_response_time = sorted(
        select_sites_with_avg_time(),
        key=lambda l: l[1],
        reverse=True,
    )
    titles = [format_long_link(site[0]) for site in default_avg_response_time]
    default_bar = [i for i in range(len(titles))]
    default_avg_values = [site[1] for site in default_avg_response_time]

    responses_by_time = select_responses_time()
    grouped_responses_time = {}
    for key, value in responses_by_time:
        if value is not None:
            grouped_responses_time.setdefault(key, []).append(value)

    percentile_90_values = [
        percentile(grouped_responses_time[site[0]], 90)
        for site in default_avg_response_time
    ]
    percentile_90_bar = [i + column_height for i in range(len(titles))]

    ax_speed.set_title("Середня швидкість відповіді сайту")
    ax_speed.set_xlabel("Швидкість (мс)")

    ax_speed.set_yticks(
        [i + column_height / 2 for i in range(len(titles))],
        titles,
    )

    ax_speed.barh(
        default_bar,
        default_avg_values,
        height=column_height,
        color="black",
        label="Середня",
    )

    ax_speed.barh(
        percentile_90_bar,
        percentile_90_values,
        height=column_height,
        color="grey",
        label="90-й перцентиль",
    )
    ax_speed.legend()


def configure_availability_graph(ax_codes):

    responses = select_responses_status_code()
    grouped_responses_status = {}
    for key, value in responses:
        if value is not None:
            grouped_responses_status.setdefault(key, []).append(value)
    responses = grouped_responses_status
    status_codes = sorted(
        {code for site_responses in responses.values() for code in site_responses}
    )

    x = list(range(len(responses)))
    width = 0.8
    bottoms = [0] * len(responses)

    for status_code in status_codes:
        values = [
            Counter(site_responses).get(status_code, 0)
            for site_responses in responses.values()
        ]

        ax_codes.bar(
            x,
            values,
            width=width,
            bottom=bottoms,
            align="center",
            label=str(status_code),
        )
        bottoms = [bottom + value for bottom, value in zip(bottoms, values)]

    titles = [format_long_link(site, width=25) for site in responses]
    ax_codes.set_xticks(list(x))
    ax_codes.set_xticklabels(titles, rotation=45, ha="center")
    ax_codes.set_xlim(-0.5, len(x) - 0.5)
    ax_codes.legend(title="Статус-код")
    ax_codes.set_title("Кількість запитів та відповідей")
    ax_codes.set_ylabel("Кількість запитів")


def configure_availability_percent_graph(ax_uptime):
    responses = {}
    for key, value in select_responses_status_code():
        if value is not None:
            responses.setdefault(key, []).append(value)
    site_avaibility = {}
    for key in responses.keys():
        site_avaibility[format_long_link(key, width=20)] = count_availability(
            responses[key]
        )
    titles = list(site_avaibility.keys())

    bar = list(range(len(titles)))

    ax_uptime.bar(
        bar,
        site_avaibility.values(),
        color="lightgrey",
        align="center",
    )

    ax_uptime.set_xticks(bar)
    ax_uptime.set_xticklabels(titles, rotation=45, ha="center")
    ax_uptime.set_xlim(-0.5, len(bar) - 0.5)
    ax_uptime.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=1))
    ax_uptime.set_title("Відсоток доступності")
    ax_uptime.set_ylabel("Відсоток")


def main():
    configure_availability_percent_graph(ax_uptime)
    configure_availability_graph(ax_codes)
    configure_avg_time_graph(ax_speed)
    plt.tight_layout()
    plt.show()
