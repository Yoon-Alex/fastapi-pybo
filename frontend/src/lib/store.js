import { writable } from 'svelte/store'

// 지속성을 지닌 스토어
const persist_storage = (key, initValue) => { // 새로고침해도 스토어 변경하지 않도록. 
    const storedValueStr = localStorage.getItem(key)
    const store = writable(storedValueStr != null ? JSON.parse(storedValueStr) : initValue)
    store.subscribe((val) => { // 스토어에 저장된 값이 변경될 때 실행되는 콜백 함수
        localStorage.setItem(key, JSON.stringify(val))
    })
    return store
}

export const page = persist_storage("page", 0) // 이름(key)과 초기값(initValue)을 입력
export const access_token = persist_storage("access_token", "")
export const username = persist_storage("username", "")
export const is_login = persist_storage("is_login", false)

// export const page = writable(0) // 초기값 0 설정

