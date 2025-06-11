function searchExercises() {
  const searchTerm = document.getElementById('searchInput').value.toLowerCase().trim(); // 앞뒤 공백 제거
  const exerciseLinks = document.querySelectorAll('.link-list a');
  const exerciseCategories = document.querySelectorAll('.link-list > div'); // 각 운동 카테고리 div

  let foundLink = null; // 검색된 첫 번째 링크를 저장할 변수

  // 먼저 모든 링크와 카테고리를 다시 보이게 처리 (재검색 시 초기화)
  exerciseLinks.forEach(link => {
    link.style.display = 'flex';
  });
  exerciseCategories.forEach(category => {
    category.style.display = 'flex';
  });


  if (searchTerm === "") {
      // 검색창이 비어있으면 모든 항목을 보이게 하고 스크롤 이동은 하지 않음
      // 이미 위에서 모두 보이게 했으므로 추가 작업 불필요
  } else {
      let isAnyLinkVisible = false;

      exerciseLinks.forEach(link => {
        const exerciseName = link.textContent.toLowerCase();
        // 검색어가 링크의 텍스트 콘텐츠에 포함되는지 확인
        if (exerciseName.includes(searchTerm)) {
          link.style.display = 'flex'; // 보이게 함
          isAnyLinkVisible = true;
          if (foundLink === null) { // 첫 번째로 검색된 링크를 저장
            foundLink = link;
          }
        } else {
          link.style.display = 'none'; // 숨김
        }
      });

      // 검색 후, 모든 링크가 숨겨진 카테고리는 숨기기
      exerciseCategories.forEach(category => {
          const visibleLinksInCategory = category.querySelectorAll('a[style*="display: flex"]');
          if (visibleLinksInCategory.length === 0) { // 보이는 링크가 없으면
              category.style.display = 'none';
          } else {
              category.style.display = 'flex'; // 아니면 보이게 함
          }
      });

      // 검색어가 있고, 검색된 링크가 있다면 해당 위치로 스크롤 이동
      if (foundLink) {
          foundLink.scrollIntoView({
              behavior: 'smooth', // 부드러운 스크롤 효과
              block: 'center'    // 요소가 뷰포트의 중앙에 오도록 스크롤
          });
      } else {
          // 검색 결과가 없는 경우, 사용자에게 피드백 제공 (선택 사항)
          // alert("검색 결과가 없습니다.");
      }
  }
}


// 초기 로드 시 모든 운동이 보이도록
window.onload = function() {
    const exerciseLinks = document.querySelectorAll('.link-list a');
    exerciseLinks.forEach(link => {
        link.style.display = 'flex';
    });
    const exerciseCategories = document.querySelectorAll('.link-list > div');
    exerciseCategories.forEach(category => {
        category.style.display = 'flex';
    });

    // 검색창에서 Enter 키를 눌렀을 때 검색 실행
    document.getElementById('searchInput').addEventListener('keypress', function(event) {
      if (event.key === 'Enter') {
        searchExercises();
      }
    });
};
