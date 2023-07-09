import pytest
from httpx import AsyncClient

from src.notes.scemas import NoteBase
from tests.response import MyResponse


@pytest.mark.parametrize('url, request_type', [
    ('/notes', 'get'),
    ('/notes/1', 'get'),
    ('/notes', 'post'),
    ('/notes/1', 'put'),
    ('/notes/1', 'delete'),
])
async def test_notes_without_access(unauthorized_client: AsyncClient,
                                    url: str, request_type: str):
    request = getattr(unauthorized_client, request_type)
    r = await request(url=url)
    MyResponse(r).assert_status_code(401).assert_json({"detail": "Unauthorized"})


async def test_get_empty_notes(authorized_client_1: AsyncClient):
    r = await authorized_client_1.get(url='/notes')
    MyResponse(r).assert_status_code(200).assert_json([])


@pytest.mark.parametrize('title, content, category_id',
                         [('Note1', 'Text', '1'),
                          ('Note2', 'Text', None)])
async def test_create_note(authorized_client_1: AsyncClient,
                           title: str, content: str, category_id: int):
    await authorized_client_1.post(url='/categories',
                                   json={'name': 'Cat1'})

    r = await authorized_client_1.post(url='/notes',
                                       json={'title': title,
                                             'content': content,
                                             'category_id': category_id})
    MyResponse(r).assert_status_code(201).validate(schema=NoteBase)


async def test_get_note(authorized_client_1: AsyncClient):
    r = await authorized_client_1.get(url='/notes/1')
    MyResponse(r).assert_status_code(200).validate(schema=NoteBase)


async def test_get_note_another_owner(authorized_client_2: AsyncClient):
    r = await authorized_client_2.get(url='/notes/1')
    MyResponse(r).assert_status_code(403).assert_json({"detail": "Access denied"})


async def test_get_note_not_found(authorized_client_1: AsyncClient):
    r = await authorized_client_1.get(url='/notes/3')
    MyResponse(r).assert_status_code(404).assert_json({"detail": "Note not found"})


async def test_get_list_notes(authorized_client_1: AsyncClient):
    r = await authorized_client_1.get(url='/notes')
    MyResponse(r).assert_status_code(200).assert_len(2).validate(schema=NoteBase)


async def test_get_list_notes_by_category(authorized_client_1: AsyncClient):
    r = await authorized_client_1.get(url='/notes', params={'category_id': 1})
    MyResponse(r).assert_status_code(200).assert_len(1).validate(schema=NoteBase)


async def test_update_note(authorized_client_1: AsyncClient):
    r = await authorized_client_1.put(url='/notes/1',
                                      json={'title': 'Note3'})
    MyResponse(r).assert_status_code(200).validate(schema=NoteBase)


async def test_update_note_another_owner(authorized_client_2: AsyncClient):
    r = await authorized_client_2.put(url='/notes/1',
                                      json={'title': 'Cat3'})
    MyResponse(r).assert_status_code(403).assert_json({"detail": "Access denied"})


async def test_update_note_not_found(authorized_client_1: AsyncClient):
    r = await authorized_client_1.get(url='/notes/3')
    MyResponse(r).assert_status_code(404).assert_json({"detail": "Note not found"})


async def test_delete_note(authorized_client_1: AsyncClient):
    r = await authorized_client_1.delete(url='/notes/2')
    MyResponse(r).assert_status_code(200).validate(schema=NoteBase)


async def test_delete_note_another_owner(authorized_client_2: AsyncClient):
    r = await authorized_client_2.delete(url='/notes/1')
    MyResponse(r).assert_status_code(403).assert_json({"detail": "Access denied"})


async def test_delete_note_not_found(authorized_client_1: AsyncClient):
    r = await authorized_client_1.delete(url='/notes/2')
    MyResponse(r).assert_status_code(404).assert_json({"detail": "Note not found"})
