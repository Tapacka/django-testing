
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
    response = client.get('/courses/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_filter_id(client, cours_factory):
    courses =  cours_factory(_quantity=10)
    response = client.get('/courses/6/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_courses_list(client, cours_factory):
    courses =  cours_factory(_quantity=10)
    response = client.get('/courses/')
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 10

@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()
    response = client.post('/courses/', data={'name': 'физика'})
    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_update_course(client, cours_factory):    
    courses = cours_factory(_quantity=1)     
    response = client.patch('/courses/23/', data={'name': 'физика'})
    resp = client.get("/courses/23/")
    assert response.status_code == 200
    assert resp.status_code == 200
    assert resp.json()['name'] == 'физика'


@pytest.mark.django_db
def test_delete_course(client, cours_factory):
    courses = cours_factory(_quantity=1)
    response = client.delete('/courses/24/')
    assert response.status_code == 204
    resp = client.get('/courses/24/')
    assert resp.status_code == 404



@pytest.mark.django_db
def test_filter_name(client):
    response = client.post('/courses/', data={'name': 'математика'})
    resp = client.get('/courses/?name="математика"')
    for i in resp.json():
        assert i['name']=='математика'

    

