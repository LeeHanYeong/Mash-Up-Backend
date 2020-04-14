# Mash-Up Backend

[![codecov](https://codecov.io/gh/LeeHanYeong/Mash-Up-Backend/branch/master/graph/badge.svg)](https://codecov.io/gh/LeeHanYeong/Mash-Up-Backend) ![CI](https://github.com/LeeHanYeong/Mash-Up-Backend/workflows/CI/badge.svg)

### - [API문서](https://mashup.lhy.kr/doc/)



## Requirements

- Python >= 3.7
- Poetry >= 1.0



## Installation

**Python packages**

```
poetry install
```



**Secrets**

> `.env` file

```
export DJANGO_SETTINGS_MODULE=config.settings.dev
```





## Test

```
pytest app
```



## Coverage (codecov.io)

> 환경변수로 `CODECOV_TOKEN`이 필요합니다

```
pytest --cov app
codecov
```

