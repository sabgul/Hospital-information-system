class NotificationsUtils {
    successPopup(text, vs) {
          const position = 'top-right';
          const progress = 'auto';
          const duration = '6000';
          const color = 'success';

          const notification = vs.notification({
              duration,
              progress,
              color,
              position,
              title: 'Hooray!🎉',
              text: text,
          });
          console.log(notification);
    }

    failPopup(e, vs) {
        const position = 'top-right';
        const progress = 'auto';
        const duration = '6000';
        const color = 'danger';

        const notification = vs.notification({
            duration,
            progress,
            color,
            position,
            title: 'Whoops!😓: ' + e.message,
            text: 'Something went wrong. Try again later or contact support.'
        });
        console.log(notification);
    }
}

export default new NotificationsUtils();