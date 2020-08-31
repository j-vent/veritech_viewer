from django.shortcuts import render
from session.models import Session, Booklet, Page, Question

def analytics(request):
    errors = {}
    scores = {}
    times = {}
    error_vals = []
    score_vals = []
    time_vals = []
    studentID_Query = request.GET.get('student_id', '')
    for i in range(1,13):
        scores[i] = []
        errors[i] = []
        times[i] = []
    print(scores)

    if studentID_Query != '':

        filtered_sessions = Session.sessions.all().filter(student_id=studentID_Query).filter(status=1)
        for session in filtered_sessions:
            num_errors = 0
            booklet_score = 0

            # months.append(session.timestamp.month);
            filtered_booklets = Booklet.booklets.all().filter(session__in=filtered_sessions)
            for booklet in filtered_booklets:
                # print(booklet.student_time_range);
                start = int(booklet.student_time_range.split(',')[0])
                end = int(booklet.student_time_range.split(',')[1])
                if(start != "" and end != ""):
                    if end < start:
                      end+= 1200
                    hours = end/100 - start/100
                    minutes = end%100 - start%100
                    time_taken = hours * 60 + minutes
                    times[session.timestamp.month].append(time_taken);

            filtered_pages = Page.pages.all().filter(booklet__in=filtered_booklets)

            for pages in filtered_pages:
                # sum up average mark of all pages in a booklet
                #scores[session.timestamp.month] += (pages.overall_mark/len(filtered_pages))/ len(scores[session.timestamp.month] +)
                scores[session.timestamp.month].append(pages.overall_mark / len(filtered_pages));

            filtered_questions = Question.questions.all().filter(page__in=filtered_pages)

            for question in filtered_questions:
                if question.marking_outcome == "REJECT":
                    num_errors += 1
            # sum up average number of errors for a booklet
            # errors[session.timestamp.month] += (num_errors/len(filtered_booklets))/ len(errors[session.timestamp.month])
            errors[session.timestamp.month].append(num_errors / len(filtered_booklets))


        for val in errors.values():
            if len(val) == 0:
                error_vals.append(0)
            else:
                error_vals.append(sum(val)/len(val))

        
        for score in scores.values():
            if len(score) == 0:
                score_vals.append(0)
            else:
                score_vals.append(sum(score)/len(score) * 100)
        print(times.values())
        for time in times.values():
            if len(time) == 0:
                time_vals.append(0)
            else:
                time_vals.append(sum(time) / len(time))
        print(time_vals)
    return render(request, "analytics.html", {'student_id': studentID_Query,
                                              'error_labels': list(errors.keys()),'error_data': error_vals,
                                              'score_labels': list(scores.keys()),'score_data': score_vals,
                                              'time_labels': list(times.keys()), 'time_data': time_vals})

