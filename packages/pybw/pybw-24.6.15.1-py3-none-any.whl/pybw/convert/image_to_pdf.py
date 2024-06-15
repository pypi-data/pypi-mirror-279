# -*- coding: utf-8 -*-
"""
author: Bowei Pu at 2023.07.27
version: 2023.08.09

Convert image files to pdf
"""

import os
import re
from glob import glob
from tqdm import tqdm
from pathlib import Path
from PIL import Image
from joblib import Parallel, delayed


def images_to_pdf(images, pdf_file, use_tqdm=True):
    """
    Convert list of images to pdf
    
    Args:
        images (list): list of image files
        pdf_file: file path of pdf to save 
        use_tqdm: if use tqdm progress bar
    
    Note:
        When prepare list of image files, do not need to judge the file type, 
        since this function will auto judge if the file can be read as image
    """
    assert pdf_file, 'arg pdf_file should not be empty'
    try:
        _ = Image
    except NameError as e:
        print('Error info: \n{}'.format(e))
        print('\nPlease import Image from PIL')
    
    if use_tqdm:
        for i, image in enumerate(tqdm(images, leave=False)):
            try:
                img = Image.open(image)
            except:
                continue
                
            if img.mode != "RGB":
                img = img.convert("RGB")
            
            if i == 0:
                img.save(pdf_file, 'PDF')
            else:
                img.save(pdf_file, 'PDF', append=True)
    else:
        for i, image in enumerate(images):
            try:
                img = Image.open(image)
            except:
                continue
                
            if img.mode != "RGB":
                img = img.convert("RGB")
            
            if i == 0:
                img.save(pdf_file, 'PDF')
            else:
                img.save(pdf_file, 'PDF', append=True)


def dir_to_pdf(dire, pdf_file='', use_tqdm=True):
    """
    Pack the use of images_to_pdf
    Auto file image files under given dire, then convert to a pdf file
    
    Args:
        dire: dire to search image files
        pdf_file: file path of pdf to save 
        use_tqdm: if use tqdm progress bar
    """
    pdf_file = pdf_file if pdf_file else Path(dire).name + '.pdf'
    # images = glob('{}/*'.format(dire))
    images = [os.path.join(dire, i) for i in os.listdir(dire)]
    images.sort()
    images_to_pdf(images, pdf_file, use_tqdm)


def get_sort_order_copymanga(name):
    name = Path(name).name
    dic = {'话': 0, '卷': 1, '番外': 2}
    key = re.findall('(c\d)(\w+)_(\d+) ', name)
    if not key:
        return ['c9', 9, '999']
    key = key[0]
    if not key[1] in dic.keys():
        return ['c9', 9, '999']
    else:
        return [key[0], dic[key[1]], key[2]]
    

def dirs_to_pdfs_copymanga_parallel(search_path='.', 
                                   book_name='new', 
                                   dire_pdf='pdfs',
                                   n_jobs=-1):
    """
    Special for copymanga, batch parallel convert dirs to pdfs
    
    Args:
        search_path: path to search sub_dire. default '.'
        book_name: comic book_name, used to rename the output pdf. 
            default 'pdfs'
        dire_pdf: dire to save the output pdf. default 'pdfs'
        n_jobs: n_jobs for Parallel. default -1
    """
    search_path = search_path.strip()
    if search_path != '.':
        finds = glob('*{}*'.format(search_path))
        if finds:
            search_path = finds[0]
            # print('    - find search_path: {}'.format(search_path))
        else:
            raise Exception('Cannot find path that match {}'.format(
                search_path))
    print('\nsearch path: {}'.format(search_path))
    
    dire_pdf = os.path.join(search_path, dire_pdf)
    if not os.path.exists(dire_pdf):
        os.makedirs(dire_pdf)
    
    # dires = [i for i in glob('{}/*'.format(search_path)) if os.path.isdir(i) and dire_pdf not in i]
    dires = [os.path.join(search_path, i) for i in os.listdir(search_path)]
    dires = [i for i in dires if os.path.isdir(i) and dire_pdf not in i]
    dires.sort(key=lambda x: get_sort_order_copymanga(x))
    print('\nfind dires:')
    for i in dires:
        print('    {}'.format(i))
    print()
    
    parallel = Parallel(n_jobs)
    _ = parallel(delayed(dir_to_pdf)(dire, 
            '{}/{} {} {}.pdf'.format(dire_pdf, book_name, 
                str(i+1).zfill(3), Path(dire).name.split()[1]), 
            False)
            for i, dire in enumerate(tqdm(dires)))


def main():
    print('\n{}'.format('-' * 50))
    print('Parallel convert image dires to pdfs for copymanga\n')
    
    search_path = input("path to search sub_dirs (default '.'): ").strip()
    book_name = input("comic name (default 'new'): ").strip()
    dire_pdf = input("output dire of pdfs (default 'pdfs'): ").strip()
    n_jobs = input("n_jobs for parallel (default '-1'): ").strip()
    
    if not search_path:
        search_path = '.'
    if not book_name:
        book_name = 'new'
    if not dire_pdf:
        dire_pdf = 'pdfs'
    if not n_jobs:
        n_jobs = -1
    
    dirs_to_pdfs_copymanga_parallel(search_path,
                                   book_name,
                                   dire_pdf,
                                   n_jobs)


if __name__ == '__main__':
    main()

    
    