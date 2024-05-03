import dayjs from 'dayjs';

export function format(date: string, formatString: string) {
    const parsedDate = dayjs(date);
    
    return parsedDate.format(formatString);
}

export function isBetween(currentDate, startDate, endDate) {
    const parsedDate = dayjs(currentDate);

    return (
        (!startDate || parsedDate.isAfter(startDate.subtract(1, 'day'), 'day')) && 
        (!endDate || parsedDate.isBefore(endDate.add(1, 'day'), 'day'))
    );
}
