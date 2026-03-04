from fastapi import Depends, HTTPException, status , Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials



security = HTTPBasic(auto_error=False)



def get_user_repo(db: AsyncSession = Depends(get_db)):
    return UserRepository(db)