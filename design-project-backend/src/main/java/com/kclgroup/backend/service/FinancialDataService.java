package com.kclgroup.backend.service;

import com.kclgroup.backend.pojo.entity.FinancialData;
import com.baomidou.mybatisplus.extension.service.IService;
import com.kclgroup.backend.pojo.vo.FinancialDataVo;

import java.util.Date;

/**
* @author 张小明
* @description 针对表【financial_data】的数据库操作Service
* @createDate 2024-06-25 16:35:57
*/
public interface FinancialDataService extends IService<FinancialData> {

    FinancialData getByStockCode(String stockCode);
    FinancialDataVo getFinancialDataByStockCode(String stockCode);
}
