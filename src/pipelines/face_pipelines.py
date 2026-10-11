import numpy as np
import dlib
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st
from src.database.db import get_all_students


@st.cache_resource  # use to run load_dlib models once only because they are too heavy
def load_dlib_models():
    # Detects where faces are in an image (bounding boxes)
    detector = dlib.get_frontal_face_detector()

    # Finds 68 facial landmarks (eyes, nose, mouth, jawline) so the face can be aligned
    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    # Deep learning model that turns an aligned face into a 128-number embedding
    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec


def get_face_embeddings(image_np):
    # Get the cached models (not reloaded on every call thanks to the decorator)
    detector, sp, facerec = load_dlib_models()

    # Detect all faces; the 1 upsamples the image once to help find smaller faces
    faces = detector(image_np, 1)

    encoding = []                    # will collect one embedding per detected face

    for face in faces:
        # Locate facial landmarks for this face
        shape = sp(image_np, face)

        # Compute the 128-d face descriptor; the 1 is the number of jitters (re-samples)
        face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1)

        encoding.append(np.array(face_descriptor))

    return encoding


# train once and reuse the model across Streamlit reruns
@st.cache_resource
def get_trained_model():
    X = []                            # face embeddings (features)
    y = []                            # student IDs (labels)

    # Load all registered students from the database
    student_db = get_all_students()

    # No students registered, so there is nothing to train on
    if not student_db:
        return None

    for student in student_db:
        embedding = student.get('face_embedding')   # stored 128-d face vector

        # Only use students who actually have an embedding saved
        if embedding:
            X.append(np.array(embedding))
            y.append(student.get('student_id'))

    # Students exist, but none have embeddings
    if len(X) == 0:
        return 0

    # Linear SVM classifier:
    #   probability=True      -> lets you get confidence scores via predict_proba
    #   class_weight='balanced' -> compensates for students with fewer samples
    clf = SVC(kernel='linear', probability=True, class_weight='balanced')

    try:
        clf.fit(X, y)                 # train: embeddings -> student IDs
    except ValueError:
        pass

    return {"clf": clf, "X": X, "Y": y}


def train_classifier():
    # Clear all cached resources so the model is rebuilt with the latest students
    st.cache_resource.clear()
    model_data = get_trained_model()
    # True if a model was built, False if None/0
    return bool(model_data)


def predict_attendance(class_image_np):
    # Get a 128-d embedding for every face in the class photo
    encodings = get_face_embeddings(class_image_np)

    detected_student = {}             # will map student_id -> detection info

    model_data = get_trained_model()

    # No trained model: nothing detected, no matches, but still report the face count
    if not model_data:
        return detected_student, [], len(encodings)

    clf = model_data['clf']           # trained SVM
    X_train = model_data['X']         # training embeddings
    y_train = model_data['Y']         # student IDs (labels)

    # Unique, sorted list of enrolled student IDs
    all_students = sorted(list(set(y_train)))

    for encoding in encodings:
        if len(all_students) >= 2:
            predicted_id = int(clf.predict([encoding])[0])
        else:
            predicted_id = int(all_students[0])

        # Stored embedding of the predicted student (first sample found for that ID)
        student_embedding = X_train[y_train.index(predicted_id)]

        # Euclidean distance between the stored face and the detected face (lower = more similar)
        best_match_score = np.linalg.norm(student_embedding - encoding)

        # 0.6 is dlib's standard cutoff for "same person"
        resemblance_threshold = 0.6

        # Only mark the student present if the face is close enough to their stored embedding
        if best_match_score <= resemblance_threshold:
            detected_student[predicted_id] = True    # student_id -> present

    # Returns: who was detected, all enrolled student IDs, and number of faces found
    return detected_student, all_students, len(encodings)
