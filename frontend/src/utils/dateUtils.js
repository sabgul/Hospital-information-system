class DateUtils {
    getDateForBackend(date) {
        const day = date.slice(8, 10);
        const month = date.slice(5, 7);
        const year = date.slice(0, 4);

        return year + '-' + month + '-' + day
    }

    getDateForFrontend(rawDate) {
        const year = rawDate.slice(0, 4);
        const month = rawDate.slice(5, 7);
        const day = rawDate.slice(8, 10);
        const time = rawDate.slice(11, 19);

        return day + '. ' + month + '. ' + year + ' ' + time;
    }
}

export default new DateUtils();