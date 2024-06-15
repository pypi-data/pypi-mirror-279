const units = [
    { unit: 'ms', multiplier: 1 },
    { unit: 's', multiplier: 1000 },
    { unit: 'm', multiplier: 60 * 1000 },
    { unit: 'h', multiplier: 60 * 60 * 1000 },
    { unit: 'd', multiplier: 24 * 60 * 60 * 1000 }
];

export function duration(milliseconds: number) {
    for (let i = units.length - 1; i >= 0; i--) {
        const { unit, multiplier } = units[i];
        const value = milliseconds / multiplier;

        if (value >= 1) {
            let significantFigures = 3;
            let formattedValue = value.toPrecision(significantFigures);

            // Remove trailing zeros and possible decimal point
            formattedValue = parseFloat(formattedValue).toString();

            return formattedValue + unit;
        }
    }

    // If duration is less than 1ms, return as is with 'ms' unit
    return milliseconds + 'ms';
}

const time_formatter = new Intl.DateTimeFormat(undefined, {
    hour: "2-digit",
    minute: "2-digit",
    hour12: true
});

export function time(date: Date) {
    return time_formatter.format(date).toLowerCase();
}
