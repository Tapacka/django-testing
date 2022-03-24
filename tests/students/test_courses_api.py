
from students.models import Student, Course
from rest_framework.test import APIClient
import pytest
from model_bakery import baker

@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory

@pytest.fixture
def cours_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory



@pytest.mark.django_db
def test_get_course(client,cours_factory):    
    courses = cours_factory(_quantity=1)
    for course in courses:
        response = client.get('/courses/', data = {'id': course.id})
        assert response.status_code == 200
        data = response.json()
        for n in data:
            assert n['name'] == course.name
    


@pytest.mark.django_db
def test_filter_id(client, cours_factory):
    courses =  cours_factory(_quantity=10)
    for cours in courses:
        response = client.get('/courses/', data = {'id': cours.id})        
        assert response.status_code == 200
        

@pytest.mark.django_db
def test_get_courses_list(client, cours_factory):
    courses = cours_factory(_quantity=10)
    response = client.get('/courses/')
    data = response.json()
    assert response.status_code == 200
    assert len(data) == len(courses)


@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()
    response = client.post('/courses/', data={'name': 'физика'})
    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_update_course(client, cours_factory):    
    courses = cours_factory(_quantity=10)
    for course in courses:     
        response = client.patch(f'/courses/{course.id}/', data={'name': 'физика'})
        resp = client.get(f'/courses/{course.id}/')
        assert response.status_code == 200
        assert resp.status_code == 200
        assert resp.json()['name'] == 'физика'


@pytest.mark.django_db
def test_delete_course(client, cours_factory):
    courses = cours_factory(_quantity=10)
    for course in courses:
        response = client.delete(f'/courses/{course.id}/')
        assert response.status_code == 204
        resp = client.get(f'/courses/{course.id}/')
        assert resp.status_code == 404



@pytest.mark.django_db
def test_filter_name(client):
    response = client.post('/courses/', data={'name': 'математика'})
    resp = client.get('/courses/?name="математика"')
    for i in resp.json():
        assert i['name']=='математика'

    

