import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the datasets
prakruti_data = pd.read_csv("prakruti_data.csv")
health_remedies_data = pd.read_csv("health_remedies_data.csv")

# Set up the Streamlit app layout
st.title("🌿 AyurSutra Chatbot 🌿")
st.sidebar.title("Choose Functionality")

# Custom CSS for Ayurvedic-themed background and styling
st.markdown(
    """
    <style>
    /* Background styling */
    .main {
        background-image: url("https://cdn.pixabay.com/photo/2017/08/01/08/29/background-2567768_1280.jpg");
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
        background-color: #e8f5e9;
    }
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: #dcedc8;
    }
    /* Button styling */
    .stButton>button {
        background-color: #558b2f;
        color: white;
        font-weight: bold;
    }
    /* Radio button styling */
    .stRadio>div>label {
        font-size: 16px;
        color: #33691e;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar option to select Prakruti assessment or Health Remedies
choice = st.sidebar.radio("Select Option:", ("Prakruti Assessment", "Health Remedies Chat"))

if choice == "Prakruti Assessment":
    st.header("Prakruti Assessment")
    
    # Initialize score counters for each dosha
    vata_score, pitta_score, kapha_score = 0, 0, 0
    
    # Iterate through questions in prakruti_data and collect responses
    for i, row in prakruti_data.iterrows():
        answer = st.radio(row['questions'], ["Yes", "No"], index=1)
        if answer == "Yes":
            vata_score += row['vata']
            pitta_score += row['pitta']
            kapha_score += row['kapha']
    
    # Display the dominant dosha based on scores
    if st.button("Get Prakruti Type"):
        # Plot a bar graph to visualize the scores
        dosha_scores = {'Vata': vata_score, 'Pitta': pitta_score, 'Kapha': kapha_score}
        st.subheader("Your Prakruti Scores")
        fig, ax = plt.subplots()
        ax.bar(dosha_scores.keys(), dosha_scores.values(), color=['#b8c1ec', '#ffcbcb', '#ffdd93'])
        plt.xlabel("Dosha Types")
        plt.ylabel("Scores")
        st.pyplot(fig)
        
        # Determine the dominant dosha
        dominant_dosha = max(dosha_scores, key=dosha_scores.get)
        st.success(f"Your dominant Prakruti type is {dominant_dosha}.")
        
        # Provide suggestions based on the dominant dosha
        st.subheader("Ayurvedic Suggestions")
        if dominant_dosha == "Vata":
            st.write("### Home Remedies:")
            st.write("- Drink warm ginger tea to balance Vata.")
            st.write("- Apply sesame oil for massages to calm the nervous system.")
            st.write("### Lifestyle Changes:")
            st.write("- Follow a consistent daily routine.")
            st.write("- Avoid cold, windy environments.")
            st.write("### Food Diet:")
            st.write("- Include warm, moist, and grounding foods like soups and stews.")
            st.write("- Avoid dry and raw foods.")
            st.write("### Yogasanas:")
            st.write("- Focus on grounding poses like Tadasana and Balasana.")
        
        elif dominant_dosha == "Pitta":
            st.write("### Home Remedies:")
            st.write("- Aloe vera juice can help cool excess Pitta.")
            st.write("- Apply sandalwood paste for a cooling effect.")
            st.write("### Lifestyle Changes:")
            st.write("- Avoid excessive heat and overexertion.")
            st.write("- Practice deep breathing exercises.")
            st.write("### Food Diet:")
            st.write("- Include cooling foods like cucumbers and melons.")
            st.write("- Avoid spicy and oily foods.")
            st.write("### Yogasanas:")
            st.write("- Focus on cooling poses like Shavasana and Sheetali Pranayama.")
        
        elif dominant_dosha == "Kapha":
            st.write("### Home Remedies:")
            st.write("- Drink warm water with honey to balance Kapha.")
            st.write("- Use eucalyptus oil for steam inhalation.")
            st.write("### Lifestyle Changes:")
            st.write("- Stay active and avoid heavy sleeping patterns.")
            st.write("- Incorporate stimulating activities into your day.")
            st.write("### Food Diet:")
            st.write("- Eat light, dry, and warm foods like legumes and vegetables.")
            st.write("- Avoid heavy, oily, and sweet foods.")
            st.write("### Yogasanas:")
            st.write("- Focus on dynamic poses like Surya Namaskar and Ustrasana.")

elif choice == "Health Remedies Chat":
    st.header("Ayurvedic Remedies Chat")
    st.write("Type in your health concerns or symptoms, and the AyurSutra Chatbot will respond with Ayurvedic recommendations.")
    
    # Create a placeholder for the chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Input box for user query
    user_input = st.text_input("You:", "")

    # Function to get recommendations
    def get_recommendation(health_issue):
        recommendations = health_remedies_data[health_remedies_data["Health Issue"] == health_issue]["Recommendation"]
        return recommendations.tolist()

    # Handle user input
    if st.button("Send"):
        if user_input:
            # Check if user input matches any health issues in the dataset
            matched_issues = health_remedies_data["Health Issue"].apply(lambda x: x.lower() in user_input.lower())
            
            if matched_issues.any():
                issue = health_remedies_data[matched_issues]["Health Issue"].values[0]
                recommendations = get_recommendation(issue)
                bot_response = f"Here are some Ayurvedic recommendations for {issue}:\n" + "\n".join([f"- {rec}" for rec in recommendations])
            else:
                bot_response = "I'm sorry, I don't have specific Ayurvedic advice for that issue at the moment."
            
            # Append user input and bot response to chat history
            st.session_state.chat_history.append({"user": user_input, "bot": bot_response})
        else:
            st.warning("Please enter a query!")

    # Display chat history
    for chat in st.session_state.chat_history:
        st.write(f"**You:** {chat['user']}")
        st.write(f"**AyurSutra Chatbot:** {chat['bot']}")
