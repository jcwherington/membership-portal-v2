import dayjs from 'dayjs';

export function isBetween(currentDate, startDate, endDate) {
    const parsedDate = dayjs(currentDate);

    return (
        (!startDate || parsedDate.isAfter(startDate.subtract(1, 'day'), 'day')) && 
        (!endDate || parsedDate.isBefore(endDate.add(1, 'day'), 'day'))
    );
}
