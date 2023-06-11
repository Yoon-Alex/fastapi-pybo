<script>
    import fastapi from "../lib/api"
    import { link } from 'svelte-spa-router' //a 태그에 use:link 속성을 사용하기 위해 link를 import를 했다.
    import { page } from "../lib/store"
    import moment from 'moment/min/moment-with-locales'
    moment.locale('ko')

    let question_list = []
    let size = 10
    // let page = 0 스벨트 스토어 변수로 대체 
    let total = 0
    $: total_page = Math.ceil(total/size)

    function get_question_list(_page) {
        let params = {
            page: _page,
            size: size,
        }
        fastapi('get', '/api/question/list', params, (json) => {
            question_list = json.question_list
            $page = _page
            total = json.total
        })
    }

    // $: page 값이 변경될 경우 get_question_list 함수도 다시 호출하라는 의미
    // https://svelte.dev/tutorial/reactive-statements
    $: get_question_list($page)
</script>

<!-- <ul>
    {#each question_list as question}
        <li><a use:link href="/detail/{question.id}">{question.subject}</a></li>
    {/each}
</ul> -->

<!-- use:link 속성을 사용한 경우는 항상 /# 문자가 선행되도록 경로가 만들어진다. 
    웹 페이지에서 어떤 경로가 /#으로 시작하면 브라우저는 이 경로를 하나의 페이지로
     인식한다. 즉, 브라우저는 http://127.0.0.1:5173/#/some-path,
      http://127.0.0.1:5173/#/question-create 두 개의 경로를 모두 
      동일한 페이지로 인식한다는 점이다. 
      이러한 것을 해시 기반 라우팅(hash based routing)이라고 한다. -->

<!-- <ul>
    {#each question_list as question}
        <li>{question.subject}</li>
    {/each}
</ul> -->

<div class="container my-3">
    <table class="table">
        <thead>
        <tr class="table-dark">
            <th>번호</th>
            <th>제목</th>
            <th>작성일시</th>
        </tr>
        </thead>
        <tbody>
        {#each question_list as question, i}
        <tr>
            <td>{ total - ($page * size) - i }</td>
            <td>
                <a use:link href="/detail/{question.id}">{question.subject}</a>
                {#if question.answers.length > 0 }
                <span class="text-danger small mx-2">{question.answers.length}</span>
                {/if}
            </td>
            <td>{moment(question.create_date).format("YYYY년 MM월 DD일 hh:mm a")}</td>
        </tr>
        {/each}
        </tbody>
    </table>
    <!-- 페이징처리 시작 -->
    <ul class="pagination justify-content-center">
        <!-- 이전페이지 -->
        <li class="page-item {$page <= 0 && 'disabled'}">
            <button class="page-link" on:click="{() => get_question_list($page-1)}">이전</button>
        </li>
        <!-- 페이지번호 -->
        {#each Array(total_page) as _, loop_page}
        {#if loop_page >= $page-5 && loop_page <= $page+5} 
        <li class="page-item {loop_page === $page && 'active'}">
            <button on:click="{() => get_question_list(loop_page)}" class="page-link">{loop_page+1}</button>
        </li>
        {/if}
        {/each}
        <!-- 다음페이지 -->
        <li class="page-item {$page >= total_page-1 && 'disabled'}">
            <button class="page-link" on:click="{() => get_question_list($page+1)}">다음</button>
        </li>
    </ul>
    <!-- 페이징처리 끝 -->    
    <a use:link href="/question-create" class="btn btn-primary">질문 등록하기</a>
</div>