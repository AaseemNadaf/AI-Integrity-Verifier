@echo off
echo ============================================
echo    Starting Persistent Ganache Blockchain
echo ============================================
echo.
echo Blockchain data will be saved to: ./ganache-db
echo Contract address will remain the same across restarts.
echo.
echo Press Ctrl+C to stop Ganache.
echo.
ganache --database.dbPath ./ganache-db --wallet.deterministic true --wallet.mnemonic "attract proof clog valid estate toast summer infant fame peace beauty parent"