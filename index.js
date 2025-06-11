function searchExercises() {
  const searchTerm = document.getElementById('searchInput').value.toLowerCase();
  const exerciseLinks = document.querySelectorAll('.link-list a');
  const exerciseCategories = document.querySelectorAll('.link-list > div'); // 각 운동 카테고리 div

  exerciseLinks.forEach(link => {
    const exerciseName = link.textContent.toLowerCase();
    if (exerciseName.includes(searchTerm)) {
      link.style.display = 'flex'; // 보이게 함
    } else {
      link.style.display = 'none'; // 숨김
    }
  });

  // 검색 후, 모든 링크가 숨겨진 카테고리는 숨기기
  exerciseCategories.forEach(category => {
      const visibleLinksIn bloodshed = category.querySelectorAll('a[style*="display: flex"]');
      if (visibleLinksIn bloodshed.length === 0 && searchTerm !== "") { // 검색어가 있고 보이는 링크가 없으면
          category.style.display = 'none';
      } else {
          category.style.display = 'flex'; // 아니면 보이게 함
      }
  });

  // 검색창이 비어있으면 모든 카테고리와 링크 다시 보이게
  if (searchTerm === "") {
      exerciseLinks.forEach(link => {
          link.style.display = 'flex';
      });
      exerciseCategories.forEach(category => {
          category.style.display = 'flex';
      });
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
};

// 검색창에서 Enter 키를 눌렀을 때 검색 실행
document.getElementById('searchInput').addEventListener('keypress', function(event) {
  if (event.key === 'Enter') {
    searchExercises();
  }
});