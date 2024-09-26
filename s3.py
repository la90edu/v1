import streamlit as st
from questions import questions  # ייבוא השאלות מקובץ חיצוני

# פונקציה להצגת שאלה סגורה עם אפשרויות
def show_closed_question(question, options, feedbacks):
    # הצגת השאלה הסגורה מהבוט
    with st.chat_message("assistant"):
        st.markdown(question)

    # יצירת כפתורים לבחירת תשובה
    cols = st.columns(len(options))
    for i, option in enumerate(options):
        if cols[i].button(option, key=f"{st.session_state.current_question}_{option}"):
            # הוספת השאלה והתשובה להיסטוריה
            st.session_state.messages.append({"role": "assistant", "content": question})
            st.session_state.messages.append({"role": "user", "content": option})
            
            # הוספת הפידבק
            st.session_state.messages.append({"role": "assistant", "content": feedbacks[i]})
            st.session_state.current_question += 1
            st.rerun()

# פונקציה להצגת שאלה פתוחה
def show_open_question(question, feedback):
    # הצגת השאלה הפתוחה מהבוט
    with st.chat_message("assistant"):
        st.markdown(question)

# פונקציה להצגת היסטוריית השיחה
def show_chat_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# פונקציה להצגת תיבת הקלט הקבועה בתחתית
def display_input_box(disabled):
    user_input = st.chat_input("הכנס את התשובה שלך כאן", disabled=disabled)
    
    if user_input:
        # אם המשתמש מקליד לאחר סיום השאלות, נוסיף להיסטוריה בלבד
        if st.session_state.current_question >= len(questions):
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.messages.append({"role": "assistant", "content": "תודה! השיחה הסתיימה, אבל אני כאן לשמוע אם יש עוד משהו שתרצה לשתף."})
        # אם המשתמש מקליד תשובה לשאלה פתוחה
        elif not disabled:
            # הוספת התשובה להיסטוריה
            st.session_state.messages.append({"role": "user", "content": user_input})

            # טיפול בשאלה הפתוחה או החזרה לשאלה הסגורה
            if st.session_state.current_question < len(questions):
                current_q = questions[st.session_state.current_question]

                # אם זו שאלה פתוחה, השאלה תטופל כאן
                if current_q["type"] == "open":
                    st.session_state.messages.append({"role": "assistant", "content": current_q["feedback"]})
                    st.session_state.current_question += 1
                # אם זו שאלה סגורה, השאלה תוצג מחדש כדי שהמשתמש יבחר באחת האפשרויות
                elif current_q["type"] == "closed":
                    st.session_state.messages.append({"role": "assistant", "content": current_q["question"]})
            
        st.rerun()

# הפונקציה הראשית
def main():
    st.title("שאלון בוט")

    # אתחול משתני session_state במידת הצורך
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        st.session_state.current_question = 0
        st.session_state.finished = False

        # הוספת משפט פתיחה
        opening_message = """
        שלום, אני ביטי הבוט של תוכנית ההייטק של משרד החינוך. נעים מאוד!
        אני כאן כדי לשמוע על הרצון והמוטיבציה שלך להשתלב בעתיד בתפקידים שונים בתעשיית ההייטק.
        נתחיל מכמה שאלות בסיסיות.
        """
        st.session_state.messages.append({"role": "assistant", "content": opening_message})

    # הצגת היסטוריית השיחה
    show_chat_history()

    # הצגת השאלה הנוכחית (אם עדיין לא סיימנו את כל השאלות)
    if not st.session_state.finished:
        if st.session_state.current_question < len(questions):
            current_q = questions[st.session_state.current_question]
            if current_q["type"] == "open":
                show_open_question(current_q["question"], current_q["feedback"])
                display_input_box(disabled=False)  # הפעלת תיבת ה-input
            elif current_q["type"] == "closed":
                show_closed_question(current_q["question"], current_q["options"], current_q["feedbacks"])
                display_input_box(disabled=True)  # השבתת תיבת ה-input
        else:
            st.session_state.finished = True
            summary_message = """
            שמחתי לשוחח איתכם ולשמוע על רמת המוטיבציה שלכם להשתלב בתחום טכנולוגי בעתיד. 
            אני ממליץ לכם בחום לדבר על הנושא עם מורה, הורה או איש צוות בבית הספר שיוכל לספר לכם עוד על התחום.
            """
            st.markdown(summary_message)
            st.session_state.messages.append({"role": "assistant", "content": summary_message})
            display_input_box(disabled=False)  # השארת תיבת ה-input פעילה גם בסוף

if __name__ == "__main__":
    main()
